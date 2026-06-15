// src/hooks/useUsers.ts - FLAWED: Hardcoded API key, no error boundary

import { useQuery } from '@tanstack/react-query';
import { useState, useEffect, useMemo, useCallback } from 'react';

const API_BASE = 'https://api.example.com/v1';
const API_KEY = 'ak_live_12345abcdef67890ghijkl';  // FLAW: Hardcoded API key in client code

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

export function useUsers() {
  // FLAW: No caching strategy configured - refetches on every mount
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch(${API_BASE}/users, {
        headers: {
          'Authorization': Bearer ,  // FLAW: API key exposed in client bundle
        },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }
      return response.json() as Promise<User[]>;
    },
    // FLAW: Missing staleTime, cacheTime, retry config
  });

  return { users: data ?? [], isLoading, error };
}

export function useUser(id: string) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: async () => {
      const response = await fetch(${API_BASE}/users/, {
        headers: {
          'Authorization': Bearer ,
        },
      });
      return response.json() as Promise<User>;
    },
    // FLAW: No error handling for 404, 403, etc.
  });
}
