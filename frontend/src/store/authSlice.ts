import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../services/api';

interface User {
    id: number;
    email: string;
    organization_id: string;
    role: string;
}

interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    loading: boolean;
    error: string | null;
}

const initialState: AuthState = {
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: !!localStorage.getItem('token'),
    loading: false,
    error: null,
};

export const login = createAsyncThunk(
    'auth/login',
    async (credentials: any, { rejectWithValue }) => {
        try {
            // Assuming URL encoded form data for OAuth2 spec compliance or JSON depending on backend
            // Backend uses OAuth2PasswordRequestForm usually, which expects form data
            // But let's check our backend implementation. It likely expects JSON compatible with OAuth2 password flow?
            // Actually standard FastAPI OAuth2PasswordRequestForm uses form-data.
            // Let's assume JSON for simplicity if we changed it, or form-data if standard.
            // Checking backend `app/auth/routes.py` -> `login_for_access_token` uses `OAuth2PasswordRequestForm`.
            // So body must be `username` and `password` form-encoded.

            const formData = new FormData();
            formData.append('username', credentials.email);
            formData.append('password', credentials.password);

            const response = await api.post('/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Login failed');
        }
    }
);

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        logout: (state) => {
            state.user = null;
            state.token = null;
            state.isAuthenticated = false;
            localStorage.removeItem('token');
        },
        setUser: (state, action: PayloadAction<User>) => {
            state.user = action.payload;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(login.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(login.fulfilled, (state, action) => {
                state.loading = false;
                state.isAuthenticated = true;
                state.token = action.payload.access_token;
                localStorage.setItem('token', action.payload.access_token);
            })
            .addCase(login.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            });
    },
});

export const { logout, setUser } = authSlice.actions;
export default authSlice.reducer;
