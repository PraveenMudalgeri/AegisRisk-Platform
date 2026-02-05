import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import assetsReducer from './slices/assetsSlice';
import risksReducer from './slices/risksSlice';
import controlsReducer from './slices/controlsSlice';
import frameworksReducer from './slices/frameworksSlice';
import { injectStore } from '../services/api';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        assets: assetsReducer,
        risks: risksReducer,
        controls: controlsReducer,
        frameworks: frameworksReducer,
    },
});

// Inject store into API interceptor
injectStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
