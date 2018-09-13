import { matchPath, RouteComponentProps } from 'react-router-dom';

/**
 * This namespace parallels our Routes object, providing useful types
 * related to specific routes.
 */
export namespace RouteTypes {
  export namespace loc {
    export namespace issues {
      export namespace area {
        export type RouteProps = RouteComponentProps<{ area: string }>;
      }
    }
  }
}

/**
 * This is an ad-hoc structure that defines URL routes for our app.
 */
const Routes = {
  /** The login page. */
  login: '/login',

  /** The logout page. */
  logout: '/logout',

  /** The home page. */
  home: '/',

  /** The onboarding flow. */
  onboarding: {
    prefix: '/onboarding',
    latestStep: '/onboarding',
    step1: '/onboarding/step/1',
    step1AddressModal: '/onboarding/step/1/address-modal',
    step2: '/onboarding/step/2',
    step2EvictionModal: '/onboarding/step/2/eviction-modal',
    step3: '/onboarding/step/3',
    step3RentStabilizedModal: '/onboarding/step/3/rent-stabilized-modal',
    step3MarketRateModal: '/onboarding/step/3/market-rate-modal',
    step3UncertainLeaseModal: '/onboarding/step/3/uncertain-lease-modal',
    step3NoLeaseModal: '/onboarding/step/3/no-lease-modal',
    step4: '/onboarding/step/4',
    step4WelcomeModal: '/onboarding/step/4/welcome-modal',
  },

  /** The Letter of Complaint flow. */
  loc: {
    prefix: '/loc',
    home: '/loc',
    whyMail: '/loc/why-mail',
    issues: {
      prefix: '/loc/issues',
      home: '/loc/issues',
      area: {
        parameterizedRoute: '/loc/issues/:area',
        create: (area: string) => `/loc/issues/${area}`,
      }
    },
    accessDates: '/loc/access-dates',
    yourLandlord: '/loc/your-landlord',
    preview: '/loc/preview',
    confirmation: '/loc/confirmation'
  },

  /** Example pages used in integration tests. */
  examples: {
    redirect: '/__example-redirect',
    modal: '/__example-modal',
    form: '/__example-form',
    loadable: '/__loadable-example-page'
  }
};

export default Routes;

/**
 * Returns if any of the arguments represents a route that
 * primarily presents the user with a modal.
 */
export function isModalRoute(...paths: string[]): boolean {
  for (let path of paths) {
    if (/-modal/.test(path)) {
      return true;
    }
  }
  return false;
}

/**
 * A class that keeps track of what routes actually exist,
 * because apparently React Router is unable to do this
 * for us.
 */
export class RouteMap {
  private existenceMap: Map<string, boolean> = new Map();
  private parameterizedRoutes: string[] = [];

  constructor(routes: any) {
    this.populate(routes);
  }

  private populate(routes: any) {
    Object.keys(routes).forEach(name => {
      const value = routes[name];
      if (typeof(value) === 'string') {
        if (value.indexOf(':') === -1) {
          this.existenceMap.set(value, true);
        } else {
          this.parameterizedRoutes.push(value);
        }
      } else if (value && typeof(value) === 'object') {
        this.populate(value);
      }
    });
  }

  get size(): number {
    return this.existenceMap.size + this.parameterizedRoutes.length;
  }

  /**
   * Given a contrete pathname, returns whether a route for it will
   * potentially match.
   * 
   * Note that it doesn't validate that route parameters are necessarily
   * valid beyond their syntactic structure, e.g. passing
   * `/objects/200` to this method may return true, but in reality there
   * may be no object with id "200". Such cases are for route handlers
   * further down the view heirarchy to resolve.
   */
  exists(pathname: string): boolean {
    if (this.existenceMap.has(pathname)) {
      return true;
    }
    for (let route of this.parameterizedRoutes) {
      const match = matchPath(pathname, { path: route });
      if (match && match.isExact) {
        return true;
      }
    }
    return false;
  }
}

export const routeMap = new RouteMap(Routes);
