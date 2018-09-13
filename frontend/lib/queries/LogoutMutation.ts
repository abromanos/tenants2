// This file was automatically generated and should not be edited.

import * as AllSessionInfo from './AllSessionInfo'
/* tslint:disable */
// This file was automatically generated and should not be edited.

import { LetterRequestMailChoice } from "./globalTypes";

// ====================================================
// GraphQL mutation operation: LogoutMutation
// ====================================================

export interface LogoutMutation_output_session_onboardingStep1 {
  name: string;
  /**
   * The user's address. Only street name and number are required.
   */
  address: string;
  aptNumber: string;
  /**
   * The New York City borough the user's address is in.
   */
  borough: string;
}

export interface LogoutMutation_output_session_onboardingStep2 {
  /**
   * Has the user received an eviction notice?
   */
  isInEviction: boolean;
  /**
   * Does the user need repairs in their apartment?
   */
  needsRepairs: boolean;
  /**
   * Is the user missing essential services like water?
   */
  hasNoServices: boolean;
  /**
   * Does the user have pests like rodents or bed bugs?
   */
  hasPests: boolean;
  /**
   * Has the user called 311 before?
   */
  hasCalled311: boolean;
}

export interface LogoutMutation_output_session_onboardingStep3 {
  /**
   * The type of lease the user has on their dwelling.
   */
  leaseType: string;
  /**
   * Does the user receive public assistance, e.g. Section 8?
   */
  receivesPublicAssistance: boolean;
}

export interface LogoutMutation_output_session_customIssues {
  area: string;
  description: string;
}

export interface LogoutMutation_output_session_landlordDetails {
  /**
   * The landlord's name.
   */
  name: string;
  /**
   * The full mailing address for the landlord.
   */
  address: string;
}

export interface LogoutMutation_output_session_letterRequest {
  updatedAt: any;
  /**
   * How the letter of complaint will be mailed.
   */
  mailChoice: LetterRequestMailChoice;
}

export interface LogoutMutation_output_session {
  /**
   * The phone number of the currently logged-in user, or null if not logged-in.
   */
  phoneNumber: string | null;
  /**
   * The cross-site request forgery (CSRF) token.
   */
  csrfToken: string;
  /**
   * Whether or not the currently logged-in user is a staff member.
   */
  isStaff: boolean;
  onboardingStep1: LogoutMutation_output_session_onboardingStep1 | null;
  onboardingStep2: LogoutMutation_output_session_onboardingStep2 | null;
  onboardingStep3: LogoutMutation_output_session_onboardingStep3 | null;
  issues: string[];
  customIssues: LogoutMutation_output_session_customIssues[];
  accessDates: string[];
  landlordDetails: LogoutMutation_output_session_landlordDetails | null;
  letterRequest: LogoutMutation_output_session_letterRequest | null;
}

export interface LogoutMutation_output {
  session: LogoutMutation_output_session;
}

export interface LogoutMutation {
  output: LogoutMutation_output;
}

export const LogoutMutation = {
  // The following query was taken from LogoutMutation.graphql.
  graphQL: `mutation LogoutMutation {
    output: logout {
        session {
            ...AllSessionInfo
        }
    }
}

${AllSessionInfo.graphQL}`,
  fetch(fetchGraphQL: (query: string, args?: any) => Promise<any>, ): Promise<LogoutMutation> {
    return fetchGraphQL(LogoutMutation.graphQL);
  }
};

export const fetchLogoutMutation = LogoutMutation.fetch;