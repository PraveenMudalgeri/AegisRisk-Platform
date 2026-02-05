import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';

export interface Control {
    id: string;
    name: string;
    description?: string;
    implementation_status: string;
    implementation_score: number;
    evidence?: string[];
}

interface ControlsState {
    items: Control[];
    loading: boolean;
    error: string | null;
}

const initialState: ControlsState = {
    items: [],
    loading: false,
    error: null,
};

export const fetchControls = createAsyncThunk(
    'controls/fetchAll',
    async (_, { rejectWithValue }) => {
        try {
            const response = await api.get('/controls/');
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch controls');
        }
    }
);

const controlsSlice = createSlice({
    name: 'controls',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchControls.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchControls.fulfilled, (state, action) => {
                state.loading = false;
                state.items = action.payload;
            })
            .addCase(fetchControls.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            });
    },
});

export default controlsSlice.reducer;
