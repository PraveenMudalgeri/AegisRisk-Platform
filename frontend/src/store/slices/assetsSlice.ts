import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';

export interface Asset {
    id: string;
    name: string;
    description?: string;
    asset_type: string;
    criticality_score: number;
    owner_id?: number;
    tags?: string[];
    created_at: string;
}

interface AssetsState {
    items: Asset[];
    loading: boolean;
    error: string | null;
}

const initialState: AssetsState = {
    items: [],
    loading: false,
    error: null,
};

export const fetchAssets = createAsyncThunk(
    'assets/fetchAll',
    async (_, { rejectWithValue }) => {
        try {
            const response = await api.get('/assets/');
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch assets');
        }
    }
);

export const createAsset = createAsyncThunk(
    'assets/create',
    async (assetData: Partial<Asset>, { rejectWithValue }) => {
        try {
            const response = await api.post('/assets/', assetData);
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to create asset');
        }
    }
);

const assetsSlice = createSlice({
    name: 'assets',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchAssets.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAssets.fulfilled, (state, action) => {
                state.loading = false;
                state.items = action.payload;
            })
            .addCase(fetchAssets.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            .addCase(createAsset.fulfilled, (state, action) => {
                state.items.push(action.payload);
            });
    },
});

export default assetsSlice.reducer;
