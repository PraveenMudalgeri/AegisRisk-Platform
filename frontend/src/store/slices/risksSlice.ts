import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';

interface RiskStats {
    overall_score_avg: number;
    total_assessments: number;
    severity_counts: Record<string, number>;
    recent_assessments: any[];
}

interface RisksState {
    stats: RiskStats | null;
    loading: boolean;
    error: string | null;
}

const initialState: RisksState = {
    stats: null,
    loading: false,
    error: null,
};

export const fetchRiskStats = createAsyncThunk(
    'risks/fetchStats',
    async (_, { rejectWithValue }) => {
        try {
            const response = await api.get('/risks/dashboard');
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch risk stats');
        }
    }
);

const risksSlice = createSlice({
    name: 'risks',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchRiskStats.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchRiskStats.fulfilled, (state, action) => {
                state.loading = false;
                state.stats = action.payload;
            })
            .addCase(fetchRiskStats.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            });
    },
});

export default risksSlice.reducer;
