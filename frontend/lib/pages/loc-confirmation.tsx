import React from 'react';

import { withAppContext, AppContextType } from '../app-context';
import { LetterRequestMailChoice } from '../queries/globalTypes';
import { AllSessionInfo_letterRequest } from '../queries/AllSessionInfo';
import Page from '../page';
import { friendlyDate } from '../util';
import { OutboundLink } from '../google-analytics';
import { PdfLink } from '../pdf-link';
import { ProgressiveLoadableConfetti } from '../confetti-loadable';

const DownloadLetterLink = (props: { locPdfURL: string }) => (
  <PdfLink href={props.locPdfURL} label="Download letter" />
);

function WeWillMailLetterStatus(props: {
  letterRequest: AllSessionInfo_letterRequest,
  locPdfURL: string
}): JSX.Element {
  const dateStr = friendlyDate(new Date(props.letterRequest.updatedAt));

  return (
    <>
      <p>We've received your request to mail a letter of complaint on <strong>{dateStr}</strong>. We'll text you a link to your <b>USPS Certified Mail<sup>&reg;</sup></b> tracking number once we have it!</p>
      <DownloadLetterLink {...props} />
      <h2>What happens next?</h2>
      <ol>
        <li>We’ll mail your letter via <b>USPS Certified Mail<sup>&reg;</sup></b> and provide a tracking number via text message.</li>
        <li>Once received, your landlord should contact you to schedule time to make repairs for the access dates you provided.</li>
        <li>While you wait, you should <strong>document your issues with photos</strong> and <strong>call 311 to request an HPD inspection.</strong></li>
        <li>We will continue to follow up with you via text message. If your landlord does not follow through, you now have better legal standing to sue your landlord. <strong>This is called an HP Action proceeding.</strong></li>
      </ol>
    </>
  );
}

function UserWillMailLetterStatus(props: { locPdfURL: string }): JSX.Element {
  return (
    <>
      <p>Here is a link to a PDF of your saved letter:</p>
      <DownloadLetterLink {...props} />
      <h2>What happens next?</h2>
      <ol>
        <li>Print out your letter and <strong>mail it via Certified Mail</strong> - this allows you to prove that it was sent to your landlord.</li>
        <li>Once received, your landlord should contact you to schedule time to make repairs for the access dates you provided.</li>
        <li>While you wait, you should <strong>document your issues with photos</strong> and <strong>call 311 to request an HPD inspection.</strong></li>
        <li>If your landlord does not follow through, you now have better legal standing to sue your landlord. <strong>This is called an HP Action proceeding.</strong></li>
      </ol>
    </>
  );
}

const knowYourRightsList = (
  <ul>
    <li><OutboundLink href="http://metcouncilonhousing.org/help_and_answers" target="_blank">MetCouncil on Housing</OutboundLink></li>
    <li><OutboundLink href="http://housingcourtanswers.org/glossary/" target="_blank">Housing Court Answers</OutboundLink></li>
  </ul>
);

const LetterConfirmation = withAppContext((props: AppContextType): JSX.Element => {
  const { letterRequest } = props.session;
  const letterStatusProps = { locPdfURL: props.server.locPdfURL };
  let letterConfirmationPageTitle, letterStatus;

  if (letterRequest && letterRequest.mailChoice === LetterRequestMailChoice.WE_WILL_MAIL) {
      letterConfirmationPageTitle = 'Your Letter of Complaint is being sent!';
      letterStatus = <WeWillMailLetterStatus letterRequest={letterRequest} {...letterStatusProps} />;
  } else {
      letterConfirmationPageTitle = 'Your Letter of Complaint has been created!';
      letterStatus = <UserWillMailLetterStatus {...letterStatusProps} />;
  }

  return (
    <Page title={letterConfirmationPageTitle}>
      <ProgressiveLoadableConfetti regenerateForSecs={1} />
      <div className="content">
        <h1 className="title">{letterConfirmationPageTitle}</h1>
        {letterStatus}
        <h2>Want to read more about your rights?</h2>
        {knowYourRightsList}
      </div>
    </Page>
  );
});

export default LetterConfirmation;
