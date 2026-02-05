import axios from 'axios';
import { RootState } from '../store';
import { Store } from '@reduxjs/toolkit';

// We'll inject store later to avoid circular dependency or just use local storage for token
let store: Store;

export const injectStore = (_store: Store) => {
    store = _store;
};

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        // Try to get token from state or localStorage
        const state = store?.getState() as RootState;
        const token = state?.auth?.token || localStorage.getItem('token');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default api;
