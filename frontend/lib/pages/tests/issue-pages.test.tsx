import React from 'react';

import { IssuesRoutes, getIssueLabel, groupByTwo } from '../issue-pages';
import Routes from '../../routes';
import { AppTesterPal } from '../../tests/app-tester-pal';
import { IssueAreaInput } from '../../queries/globalTypes';
import { IssueAreaMutation_output } from '../../queries/IssueAreaMutation';
import ISSUE_AREA_SVGS from '../../svg/issues';
import { IssueAreaChoices } from '../../../../common-data/issue-area-choices';


const routes = Routes.locale.loc.issues;

const TestIssuesRoutes = () => 
  <IssuesRoutes routes={Routes.locale.loc.issues} toBack="back" toNext="next"/>;

describe('issues checklist', () => {
  afterEach(AppTesterPal.cleanup);

  it('returns 404 for invalid area routes', () => {
    const pal = new AppTesterPal(<TestIssuesRoutes />, {
      url: routes.area.create('LOL')
    });
    pal.rr.getByText('Alas.');
  });

  it('works on valid area routes', async () => {
    const pal = new AppTesterPal(<TestIssuesRoutes />, {
      url: routes.area.create('HOME'),
      session: {
        issues: ['BEDROOMS__PAINT']
      }
    });
    pal.clickRadioOrCheckbox(/Mice/i);
    pal.clickButtonOrLink('Save');

    pal.expectFormInput<IssueAreaInput>({
      area: 'HOME', issues: ['HOME__MICE'], other: ''
    });
    pal.respondWithFormOutput<IssueAreaMutation_output>({
      errors: [],
      session: { issues: ['HOME__MICE'], customIssues: [] }
    });
    await pal.rt.waitForElement(() => pal.rr.getByText('Apartment self-inspection'));
  });
});

test('getIssueLabel() works', () => {
  expect(getIssueLabel(0)).toBe('No issues reported');
  expect(getIssueLabel(1)).toBe('One issue reported');
  expect(getIssueLabel(2)).toBe('2 issues reported');
  expect(getIssueLabel(99)).toBe('99 issues reported');
});

test('issue area images exist', () => {
  IssueAreaChoices.forEach(area => {
    const svg = ISSUE_AREA_SVGS[area];
    if (!svg) {
      throw new Error(`Expected ISSUE_AREA_SVGS.${area} to exist`);
    }
  });
});

test('groupByTwo() works', () => {
  expect(groupByTwo([1])).toEqual([[1, null]]);
  expect(groupByTwo([1, 2])).toEqual([[1, 2]]);
  expect(groupByTwo([1, 2, 3])).toEqual([[1, 2], [3, null]]);
});
