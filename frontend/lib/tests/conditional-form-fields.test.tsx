import React from 'react';

import ReactTestingLibraryPal from "./rtl-pal";
import { fakeBaseFieldProps } from "./form-fields.test";
import { hideByDefault, ConditionalYesNoRadiosFormField } from "../conditional-form-fields";
import { BaseFormFieldProps } from '../form-fields';
import { FormError } from '../form-errors';

test("hideByDefault() works", () => {
  expect(hideByDefault(fakeBaseFieldProps({ value: '' })).hidden).toBe(true);
});

describe("ConditionalYesNoRadiosFormField", () => {
  const create = (hidden: boolean, props: Partial<BaseFormFieldProps<string>>) => (
    new ReactTestingLibraryPal(
      <ConditionalYesNoRadiosFormField {...fakeBaseFieldProps({
        ...props,
        value: ''
      })} hidden={hidden} label="Please answer this yes/no question" />
    )
  );
  const createHidden = create.bind(null, true);
  const createVisible = create.bind(null, false);

  afterEach(ReactTestingLibraryPal.cleanup);

  it("can be hidden", () => {
    const pal = createHidden({});
    pal.getElement('input', '[type="hidden"]');
  });

  it("can be shown", () => {
    const pal = createVisible({});
    pal.getFormField('Yes');
  });

  it("is forcibly shown if errors are present", () => {
    const pal = createHidden({
      errors: [new FormError('blah')]
    });
    pal.getFormField('Yes');
  });
});
