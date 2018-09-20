/** @jest-environment node */

import { Readable } from 'stream';

import { errorCatchingHandler, handleFromJSONStream, LambdaResponse, isPlainJsObject } from '../lambda';
import { AppProps } from '../../lib/app';
import { FakeServerInfo, FakeSessionInfo } from '../../lib/tests/util';

const fakeAppProps: AppProps = {
  initialURL: '/',
  server: FakeServerInfo,
  initialSession: FakeSessionInfo
};

test('lambda works', async () => {
  jest.setTimeout(10000);
  const response = await errorCatchingHandler(fakeAppProps);
  expect(response.status).toBe(200);
  expect(response.location).toBeNull();
});

test('lambda redirects', async () => {
  const response = await errorCatchingHandler({
    ...fakeAppProps,
    initialURL: '/__example-redirect'
  });
  expect(response.status).toBe(302);
  expect(response.location).toBe('/');
});

test('lambda catches errors', async () => {
  const response = await errorCatchingHandler({
    ...fakeAppProps,
    testInternalServerError: true
  });
  expect(response.status).toBe(500);
  expect(response.traceback).toMatch(/Testing internal server error/i);
  expect(response.traceback).toMatch(/lambda\.tsx/);
});

test('isPlainJsObject works', () => {
  expect(isPlainJsObject(null)).toBe(false);
  expect(isPlainJsObject([])).toBe(false);
  expect(isPlainJsObject({})).toBe(true);
});

describe('handleFromJSONStream', () => {
  const makeStream = (thing: any) => {
    const stream = new Readable();
    let text = typeof(thing) === 'string' ? thing : JSON.stringify(thing);
    stream.push(Buffer.from(text, 'utf-8'));
    stream.push(null);
    return stream;
  }

  const handle = async (thing: any) => {
    const response = await handleFromJSONStream(makeStream(thing));
    return JSON.parse(response.toString('utf-8')) as LambdaResponse;
  }

  it('works', async () => {
    const response = await handle(fakeAppProps);
    expect(response.status).toBe(200);
  });

  it('raises error on malformed input', () => {
    const response = handle('i am not valid json');
    expect(response).rejects.toBeInstanceOf(SyntaxError);
  });

  it('raises error on bad JSON input', () => {
    const response = handle(null);
    expect(response).rejects.toEqual(new Error("Expected input to be a JS object!"));
  });
});
