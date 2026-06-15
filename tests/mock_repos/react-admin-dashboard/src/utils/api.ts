// src/utils/api.ts - FLAWED: API utility with security issues

const API_BASE = process.env.REACT_APP_API_BASE || 'https://api.example.com/v1';

interface RequestOptions extends RequestInit {
  params?: Record<string, string>;
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { params, ...fetchOptions } = options;

  let url = ${API_BASE};
  if (params) {
    // FLAW: No URL encoding of params - potential injection
    const queryString = Object.entries(params)
      .map(([key, value]) => ${key}=)  // FLAW: Should use encodeURIComponent
      .join('&');
    url += ?;
  }

  // FLAW: Credentials always included - should be configurable
  const response = await fetch(url, {
    ...fetchOptions,
    credentials: 'include',  // FLAW: Always sends cookies, even cross-origin
  });

  // FLAW: No content-type validation
  // FLAW: No timeout handling
  if (!response.ok) {
    // FLAW: Error response body may contain sensitive info exposed to client
    const errorBody = await response.text();
    throw new Error(errorBody);  // FLAW: Leaks server error details to UI
  }

  return response.json() as Promise<T>;
}

// FLAW: Convenience functions without type safety
export const get = (url: string, params?: Record<string, string>) =>
  apiRequest(url, { method: 'GET', params });

export const post = (url: string, body: any) =>  // FLAW: 'any' type for body
  apiRequest(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

export const put = (url: string, body: any) =>
  apiRequest(url, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

export const del = (url: string) =>
  apiRequest(url, { method: 'DELETE' });
