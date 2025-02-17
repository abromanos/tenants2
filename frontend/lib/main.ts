/// <reference path="main-globals.d.ts" />

import { startApp, AppProps } from './app';
import { getElement } from './util';
import { ga } from './google-analytics';
import i18n from './i18n';


function polyfillSmoothScroll() {
  if (document.documentElement &&
      !('scrollBehavior' in document.documentElement.style)) {
    import(/* webpackChunkName: "smoothscroll-polyfill" */ 'smoothscroll-polyfill')
      .then((smoothscroll) => smoothscroll.polyfill());
  }
}

function showSafeModeUiOnShake() {
  if (!('ondevicemotion' in window)) return;

  import(/* webpackChunkName: "shake" */ '../vendor/shake')
    .then((exports) => {
      const Shake = exports.default;

      new Shake({ threshold: 15, timeout: 1000 }).start();

      window.addEventListener('shake', () => {
        ga('send', 'event', 'motion', 'shake');
        window.SafeMode.showUI();
      }, false);
    });
}

window.addEventListener('load', () => {
  const div = getElement('div', '#main');
  const initialPropsEl = getElement('script', '#initial-props');
  if (!initialPropsEl.textContent) {
    throw new Error('Assertion failure, #initial-props must contain text');
  }
  const initialProps = JSON.parse(initialPropsEl.textContent) as AppProps;

  // See main-globals.d.ts for more details on this.
  __webpack_public_path__  = initialProps.server.webpackPublicPathURL;

  // It's possible that the server-side has made our main div
  // hidden because a pre-rendered modal is intended to contain
  // all keyboard-focusable elements in case JS couldn't be loaded.
  // Since JS is now loaded, let's remove that restriction.
  div.removeAttribute('hidden');

  i18n.initialize(initialProps.locale);
  startApp(div, initialProps);
  polyfillSmoothScroll();
  showSafeModeUiOnShake();
});

if (process.env.NODE_ENV !== 'production' && DISABLE_DEV_SOURCE_MAPS) {
  console.log(
    'Source maps have been disabled to improve compilation speed. To ' +
    'prevent this, unset the DISABLE_DEV_SOURCE_MAPS ' +
    'environment variable.'
  );
}
