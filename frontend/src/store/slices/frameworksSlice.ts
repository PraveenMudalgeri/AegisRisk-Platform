import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';

interface FrameworkCoverage {
    [key: string]: {
        covered: number;
        total: number;
        percentage: number;
    };
}

interface FrameworksState {
    coverage: FrameworkCoverage | null;
    loading: boolean;
    error: string | null;
}

const initialState: FrameworksState = {
    coverage: null,
    loading: false,
    error: null,
};

export const fetchCoverage = createAsyncThunk(
    'frameworks/assessCoverage',
    async (_, { rejectWithValue }) => {
        try {
            const response = await api.post('/mappings/assess');
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch coverage');
        }
    }
);

const frameworksSlice = createSlice({
    name: 'frameworks',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchCoverage.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchCoverage.fulfilled, (state, action) => {
                state.loading = false;
                state.coverage = action.payload;
            })
            .addCase(fetchCoverage.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            });
    },
});

export default frameworksSlice.reducer;
