import React from 'react';
import { ga, trackPageView, OutboundLink, handleOutboundLinkClick } from "../google-analytics";
import ReactTestingLibraryPal from "./rtl-pal";
import { setHardRedirector } from './hard-redirect';

describe('ga()', () => {
  describe('if window.ga is undefined', () => {
    beforeEach(() => {
      delete window.ga;
      jest.useFakeTimers();
    });

    it('does not explode', () => {
      ga('set', 'page', '/blah');
    });

    it('calls any hit callbacks almost immediately', () => {
      const hitCallback = jest.fn();
      ga('send', 'event', 'outbound', 'click', 'https://boop.com/', {
        transport: 'beacon',
        hitCallback
      });
      expect(hitCallback.mock.calls).toHaveLength(0);
      jest.advanceTimersByTime(10);
      expect(hitCallback.mock.calls).toHaveLength(1);
    });
  });

  it('calls window.ga if it is defined', () => {
    const mockGa = jest.fn();
    window.ga = mockGa;
    ga('set', 'page', '/blah');
    expect(mockGa.mock.calls).toHaveLength(1);
    expect(mockGa.mock.calls[0]).toEqual(['set', 'page', '/blah']);
    delete window.ga;
  });
});

test('helper functions do not explode', () => {
  trackPageView('/blah');
});

describe('OutboundLink', () => {
  const gaMock = jest.fn();
  const hardRedirect = jest.fn();
  const callHitCallback = () => {
    gaMock.mock.calls[0][5].hitCallback();
  };

  beforeEach(() => {
    jest.useFakeTimers();
    window.ga = gaMock;
    setHardRedirector(hardRedirect);
    gaMock.mockReset();
    hardRedirect.mockReset();
  });

  it('sends hit to GA on click and then redirects', () => {
    const pal = new ReactTestingLibraryPal(
      <OutboundLink href="https://boop.com/">boop</OutboundLink>
    );
    pal.clickButtonOrLink('boop');
    expect(gaMock.mock.calls).toHaveLength(1);
    expect(gaMock.mock.calls[0].slice(0, 5)).toEqual([
      'send', 'event', 'outbound', 'click', 'https://boop.com/'
    ]);

    jest.advanceTimersByTime(400);
    expect(hardRedirect.mock.calls).toHaveLength(0);
    callHitCallback();
    expect(hardRedirect.mock.calls).toEqual([['https://boop.com/']]);
  });

  it('opens link in a new window if "target" prop is set', () => {
    const mockOpen = jest.fn();
    window.open = mockOpen;
    const pal = new ReactTestingLibraryPal(
      <OutboundLink href="https://bap.com/" target="_blank">bap</OutboundLink>
    );
    pal.clickButtonOrLink('bap');
    callHitCallback();
    expect(hardRedirect.mock.calls).toHaveLength(0);
    expect(mockOpen.mock.calls).toEqual([['https://bap.com/', '_blank']]);
  });

  it('redirects after a timeout if GA has not responded', () => {
    const pal = new ReactTestingLibraryPal(
      <OutboundLink href="https://blorp.com/">blorp</OutboundLink>
    );
    pal.clickButtonOrLink('blorp');
    jest.advanceTimersByTime(1001);
    expect(hardRedirect.mock.calls).toEqual([['https://blorp.com/']]);
  });

  it('prevents default click behavior when using GA', () => {
    const preventDefault = jest.fn();
    const e = { currentTarget: { href: 'blah' }, preventDefault } as any;
    handleOutboundLinkClick(e);
    expect(gaMock.mock.calls).toHaveLength(1);
    expect(preventDefault.mock.calls).toHaveLength(1);
  });

  it('does nothing when a modifier key is pressed', () => {
    const preventDefault = jest.fn();
    const e = { shiftKey: true, preventDefault } as any;
    handleOutboundLinkClick(e);
    expect(gaMock.mock.calls).toHaveLength(0);
    expect(preventDefault.mock.calls).toHaveLength(0);
  });
});
