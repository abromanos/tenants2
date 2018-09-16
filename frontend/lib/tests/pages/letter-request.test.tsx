import React from 'react';
import Routes from '../../routes';
import { AppTesterPal } from '../app-tester-pal';
import LetterOfComplaintRoutes from '../../letter-of-complaint';
import { LetterRequestMutation_output } from '../../queries/LetterRequestMutation';
import { LetterRequestMailChoice } from '../../queries/globalTypes';


describe('landlord details page', () => {
  afterEach(AppTesterPal.cleanup);

  it('redirects to next step after successful submission', async () => {
    const pal = new AppTesterPal(<LetterOfComplaintRoutes />, {
      url: Routes.loc.preview,
    });
    pal.clickButtonOrLink('Finish');
    const updatedAt = "2018-01-01Tblahtime";
    const mailChoice = LetterRequestMailChoice.WE_WILL_MAIL;
    pal.respondWithFormOutput<LetterRequestMutation_output>({
      errors: [],
      session: { letterRequest: { updatedAt, mailChoice } }
    });

    await pal.rt.waitForElement(() => pal.rr.getByText(/Your letter of complaint has been created/i));
    const { mock } = pal.appContext.updateSession;
    expect(mock.calls).toHaveLength(1);
    expect(mock.calls[0][0]).toEqual({ letterRequest: { updatedAt, mailChoice } });
  });
});
