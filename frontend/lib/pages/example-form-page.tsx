import React from 'react';

import Page from "../page";
import { LegacyFormSubmitter } from '../legacy-form-submitter';
import { ExampleMutation, BlankExampleInput, BlankSubformsExampleSubformFormSetInput } from '../queries/ExampleMutation';
import { TextualFormField, CheckboxFormField } from '../form-fields';
import { NextButton } from '../buttons';
import Routes from '../routes';
import { ExampleInput } from '../queries/globalTypes';
import { Modal, BackOrUpOneDirLevel, ModalLink } from '../modal';
import { Formset } from '../formset';
import { CurrencyFormField } from '../currency-form-field';
import { ProgressiveOtherCheckboxFormField } from '../other-checkbox-form-field';

const INITIAL_STATE: ExampleInput = {
  ...BlankExampleInput,
  currencyField: '15.00',
};

/* istanbul ignore next: this is tested by integration tests. */
function FormInModal(): JSX.Element {
  return (
    <Modal title="Example form in a modal" onCloseGoTo={BackOrUpOneDirLevel} render={() => <>
      <p>Here's the same form, but in a modal!</p>
      <ExampleForm onSuccessRedirect={Routes.dev.examples.form} id="in_modal" />
    </>}/>
  );
}

/* istanbul ignore next: this is tested by integration tests. */
function ExampleForm(props: { id: string, onSuccessRedirect: string }): JSX.Element {
  return (
    <LegacyFormSubmitter
      mutation={ExampleMutation}
      initialState={INITIAL_STATE}
      onSuccessRedirect={props.onSuccessRedirect}
      formId={props.id}
    >
      {(ctx) => (
        <React.Fragment>
          {ctx.nonFieldErrors &&
           ctx.nonFieldErrors.some(nfe => nfe.code === 'CODE_NFOER') &&
           <p className="has-grey-light">
             An error with code <code>CODE_NFOER</code> is present.
           </p>}
          <TextualFormField label="Example field" {...ctx.fieldPropsFor('exampleField')} />
          <CheckboxFormField {...ctx.fieldPropsFor('boolField')}>
            Example boolean field
          </CheckboxFormField>
          <ProgressiveOtherCheckboxFormField {...ctx.fieldPropsFor('exampleOtherField')}
            baselineLabel="If you have anything else to report, please specify it."
            enhancedLabel="Please specify."
          />
          <CurrencyFormField label="Example currency field" {...ctx.fieldPropsFor('currencyField')}/>
          <Formset {...ctx.formsetPropsFor('subforms')} emptyForm={BlankSubformsExampleSubformFormSetInput}>
            {(subforms, i) => (
              <TextualFormField label={`example subform field #${i + 1}`} {...subforms.fieldPropsFor('exampleField')} />
            )}
          </Formset>
          <div className="field">
            <NextButton isLoading={ctx.isLoading} label="Submit" />
          </div>
        </React.Fragment>
      )}
    </LegacyFormSubmitter>
  );
}

/* istanbul ignore next: this is tested by integration tests. */
export default function ExampleFormPage(): JSX.Element {
  return (
    <Page title="Example form page">
      <div className="content">
        <p>This is an example form page.</p>
        <ModalLink to={Routes.dev.examples.formInModal} component={FormInModal} className="button is-light">
          Use the form in a modal
        </ModalLink>
      </div>
      <ExampleForm onSuccessRedirect={Routes.locale.home} id="not_in_modal" />
    </Page>
  );
}
