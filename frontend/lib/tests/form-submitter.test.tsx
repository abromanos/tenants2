import React from 'react';
import { MyFormInput, MyFormOutput, myInitialState, renderMyFormFields } from './my-form';
import { createTestGraphQlClient, simpleFormErrors } from './util';
import { shallow, mount } from 'enzyme';
import { FormSubmitterWithoutRouter, FormSubmitter } from '../form-submitter';
import { MemoryRouter, Switch, Route } from 'react-router';

describe('FormSubmitter', () => {
  const payload: MyFormInput = { phoneNumber: '1', password: '2' };

  const buildForm = () => {
    const { client } = createTestGraphQlClient();
    const onSuccess = jest.fn();

    const wrapper = shallow(
      <FormSubmitterWithoutRouter
        history={null as any}
        location={null as any}
        match={null as any}
        onSubmit={(input: MyFormInput) => client.fetch('blah', { input }).then(r => r.login) }
        onSuccess={(output: MyFormOutput) => { onSuccess(output); }}
        initialState={myInitialState}
      >
        {renderMyFormFields}
      </FormSubmitterWithoutRouter>
    );
    const form = wrapper.instance() as FormSubmitterWithoutRouter<MyFormInput, MyFormOutput>;
    return { form, client, onSuccess };
  };

  it('optionally uses performRedirect() for redirection', async () => {
    const promise = Promise.resolve({ errors: [] });
    const performRedirect = jest.fn();
    const wrapper = mount(
      <MemoryRouter>
        <Switch>
          <Route>
            <FormSubmitter
              onSubmit={() => promise}
              onSuccess={() => {}}
              onSuccessRedirect="/blah"
              performRedirect={performRedirect}
              initialState={myInitialState}
              children={renderMyFormFields} />
          </Route>
        </Switch>
      </MemoryRouter>
    );
    wrapper.find('form').simulate('submit');
    await promise;
    expect(performRedirect.mock.calls).toHaveLength(1);
    expect(performRedirect.mock.calls[0][0]).toBe('/blah');
  });

  it('optionally calls onSuccess(), then redirects when successful', async () => {
    const promise = Promise.resolve({ errors: [] });
    const glob = { word: "foo" };
    const BlahPage = () => <p>This is {glob.word}.</p>;
    const wrapper = mount(
      <MemoryRouter>
        <Switch>
          <Route path="/blah" exact component={BlahPage}/>
          <Route>
            <FormSubmitter
              onSubmit={() => promise}
              onSuccess={() => { glob.word = "blah"; }}
              onSuccessRedirect="/blah"
              initialState={myInitialState}
              children={renderMyFormFields} />
          </Route>
        </Switch>
      </MemoryRouter>
    );
    wrapper.find('form').simulate('submit');
    await promise;
    expect(wrapper.html()).toBe('<p>This is blah.</p>');
  });

  it('sets state when successful', async () => {
    const { form, client, onSuccess } = buildForm();
    const login = form.handleSubmit(payload);

    expect(form.state.isLoading).toBe(true);
    client.getRequestQueue()[0].resolve({
      login: {
        errors: [],
        session: 'blehhh'
      }
    });
    await login;
    expect(form.state.isLoading).toBe(false);
    expect(onSuccess.mock.calls).toHaveLength(1);
    expect(onSuccess.mock.calls[0][0]).toEqual({ errors: [], session: 'blehhh' });
  });

  it('sets state when validation errors occur', async () => {
    const { form, client, onSuccess } = buildForm();
    const login = form.handleSubmit(payload);

    expect(form.state.isLoading).toBe(true);
    client.getRequestQueue()[0].resolve({
      login: {
        errors: [{
          field: '__all__',
          extendedMessages: [{ message: 'nope.', code: null }]
        }]
      }
    });
    await login;
    expect(form.state.isLoading).toBe(false);
    expect(form.state.errors).toEqual({
      nonFieldErrors: simpleFormErrors('nope.'),
      fieldErrors: {}
    });
    expect(onSuccess.mock.calls).toHaveLength(0);
  });

  it('sets state when network error occurs', async () => {
    const { form, client, onSuccess } = buildForm();
    const login = form.handleSubmit(payload);

    client.getRequestQueue()[0].reject(new Error('kaboom'));
    await login;
    expect(form.state.isLoading).toBe(false);
    expect(onSuccess.mock.calls).toHaveLength(0);
  });
});
