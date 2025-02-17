import React from 'react';
import Loadable from 'react-loadable';
import { Route } from 'react-router';

import { OnboardingInfoSignupIntent } from "./queries/globalTypes";
import { AllSessionInfo_onboardingInfo } from "./queries/AllSessionInfo";
import { getSignupIntentOnboardingInfo } from './routes';
import { LoadingPage, friendlyLoad } from './loading-page';

/** The default assumed intent if none is explicitly provided. */
export const DEFAULT_SIGNUP_INTENT_CHOICE = OnboardingInfoSignupIntent.LOC;

const LoadableOnboardingRoutes = Loadable({
  loader: () => friendlyLoad(import(/* webpackChunkName: "onboarding" */ './onboarding')),
  loading: LoadingPage
});

export function signupIntentFromOnboardingInfo(onboardingInfo: AllSessionInfo_onboardingInfo|null): OnboardingInfoSignupIntent {
  if (!onboardingInfo) return DEFAULT_SIGNUP_INTENT_CHOICE;
  return onboardingInfo.signupIntent;
}

/**
 * Return a <Route> that contains all the onboarding routes for the given intent.
 * 
 * Note that this is explicitly *not* a component because we want to be able to
 * include this in a <Switch>, which needs <Route> components as its
 * immediate children.
 */
export function getOnboardingRouteForIntent(intent: OnboardingInfoSignupIntent): JSX.Element {
  const info = getSignupIntentOnboardingInfo(intent);
  return <Route
    path={info.onboarding.prefix}
    render={() => (
      <LoadableOnboardingRoutes
        routes={info.onboarding}
        toCancel={info.preOnboarding}
        toSuccess={info.postOnboarding}
        signupIntent={intent}
      />
    )}
  />;
}
