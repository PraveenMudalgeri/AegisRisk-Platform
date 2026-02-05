import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { fetchControls } from '../store/slices/controlsSlice';
import { FileCheck, CheckCircle2, Circle } from 'lucide-react';

const Controls: React.FC = () => {
    const dispatch = useDispatch<AppDispatch>();
    const { items } = useSelector((state: RootState) => state.controls);

    useEffect(() => {
        dispatch(fetchControls());
    }, [dispatch]);

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-white">Security Controls</h1>
                <p className="text-gray-400">Monitor implementation status of required controls</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {items.map((control) => (
                    <div key={control.id} className="glass p-5 rounded-2xl border border-white/10 hover:border-primary/50 transition-all group">
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-2 bg-emerald-500/10 rounded-lg text-emerald-500">
                                <FileCheck size={24} />
                            </div>
                            {control.implementation_status === 'IMPLEMENTED' ? (
                                <CheckCircle2 className="text-emerald-500" />
                            ) : (
                                <Circle className="text-gray-600" />
                            )}
                        </div>

                        <h3 className="text-white font-semibold mb-2">{control.name}</h3>
                        <p className="text-gray-400 text-sm mb-4 line-clamp-2">{control.description || 'No description provided.'}</p>

                        <div className="flex justify-between items-center text-xs mt-4 pt-4 border-t border-white/5">
                            <span className="text-gray-500">Score: {control.implementation_score}</span>
                            <span className={`px-2 py-1 rounded ${control.implementation_status === 'IMPLEMENTED' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-gray-700 text-gray-400'}`}>
                                {control.implementation_status}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Controls;
