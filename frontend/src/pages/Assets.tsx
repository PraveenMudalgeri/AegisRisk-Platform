import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { fetchAssets } from '../store/slices/assetsSlice';
import { Database, Plus, Play, MoreHorizontal } from 'lucide-react';
import api from '../services/api';

const Assets: React.FC = () => {
    const dispatch = useDispatch<AppDispatch>();
    const { items, loading } = useSelector((state: RootState) => state.assets);

    useEffect(() => {
        dispatch(fetchAssets());
    }, [dispatch]);

    const handleAssessRisk = async (assetId: string) => {
        try {
            // Trigger enumeration and then assessment
            await api.post(`/risks/threats/enumerate/${assetId}`);
            await api.post(`/risks/assess/${assetId}`);
            alert('Risk assessment triggered successfully!');
        } catch (e) {
            alert('Failed to trigger assessment');
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white">Assets</h1>
                    <p className="text-gray-400">Manage infrastructure and data assets</p>
                </div>
                <button className="bg-primary hover:bg-cyan-400 text-white px-4 py-2 rounded-xl flex items-center shadow-lg shadow-primary/20 transition-all">
                    <Plus size={18} className="mr-2" />
                    New Asset
                </button>
            </div>

            <div className="glass rounded-2xl border border-white/10 overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-white/5 text-gray-400">
                        <tr>
                            <th className="px-6 py-4 font-medium">Asset Name</th>
                            <th className="px-6 py-4 font-medium">Type</th>
                            <th className="px-6 py-4 font-medium">Criticality</th>
                            <th className="px-6 py-4 font-medium">Owner</th>
                            <th className="px-6 py-4 font-medium">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {items.map((asset) => (
                            <tr key={asset.id} className="hover:bg-white/5 transition-colors">
                                <td className="px-6 py-4">
                                    <div className="flex items-center">
                                        <div className="h-10 w-10 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center mr-3">
                                            <Database size={20} />
                                        </div>
                                        <div className="font-medium text-white">{asset.name}</div>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-gray-300">{asset.asset_type}</td>
                                <td className="px-6 py-4">
                                    <div className="w-24 bg-gray-700 h-2 rounded-full overflow-hidden">
                                        <div className="bg-gradient-to-r from-emerald-500 to-amber-500 h-full" style={{ width: `${asset.criticality_score}%` }}></div>
                                    </div>
                                    <span className="text-xs text-gray-500 mt-1 block">{asset.criticality_score}/100</span>
                                </td>
                                <td className="px-6 py-4 text-gray-400">Unassigned</td>
                                <td className="px-6 py-4">
                                    <div className="flex items-center space-x-2">
                                        <button
                                            onClick={() => handleAssessRisk(asset.id)}
                                            className="p-2 hover:bg-primary/20 hover:text-primary rounded-lg transition-colors text-gray-400"
                                            title="Run Risk Assessment"
                                        >
                                            <Play size={18} />
                                        </button>
                                        <button className="p-2 hover:bg-white/10 rounded-lg transition-colors text-gray-400">
                                            <MoreHorizontal size={18} />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {items.length === 0 && !loading && (
                    <div className="text-center py-12 text-gray-500">
                        No assets found. Create one to get started.
                    </div>
                )}
            </div>
        </div>
    );
};

export default Assets;
