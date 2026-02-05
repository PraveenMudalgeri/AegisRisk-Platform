import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { fetchCoverage } from '../store/slices/frameworksSlice';
import { BookOpen, ExternalLink, ChevronDown } from 'lucide-react';

const Frameworks: React.FC = () => {
    const dispatch = useDispatch<AppDispatch>();
    const { coverage } = useSelector((state: RootState) => state.frameworks);

    useEffect(() => {
        dispatch(fetchCoverage());
    }, [dispatch]);

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-white">Compliance Frameworks</h1>
                <p className="text-gray-400">Track alignment with standard regulations</p>
            </div>

            <div className="space-y-4">
                {coverage && Object.entries(coverage).map(([framework, stats]) => (
                    <div key={framework} className="glass rounded-2xl overflow-hidden border border-white/10">
                        <div className="p-6 flex items-center justify-between cursor-pointer hover:bg-white/5 transition-colors">
                            <div className="flex items-center space-x-4">
                                <div className="h-12 w-12 rounded-xl bg-blue-500/20 text-blue-400 flex items-center justify-center">
                                    <BookOpen size={24} />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-white">{framework}</h3>
                                    <p className="text-sm text-gray-400">International Standard</p>
                                </div>
                            </div>

                            <div className="flex items-center space-x-8">
                                <div className="text-right">
                                    <div className="text-2xl font-bold text-white">{stats.percentage}%</div>
                                    <div className="text-xs text-gray-500">Coverage</div>
                                </div>
                                <div className="h-12 w-12 flex items-center justify-center rounded-full bg-white/5">
                                    <ChevronDown className="text-gray-400" />
                                </div>
                            </div>
                        </div>

                        {/* Progress Bar */}
                        <div className="h-1 bg-gray-800 w-full">
                            <div className="h-full bg-blue-500 transition-all duration-1000" style={{ width: `${stats.percentage}%` }}></div>
                        </div>

                        <div className="p-6 bg-black/20 grid grid-cols-3 gap-4 border-t border-white/5">
                            <div className="bg-white/5 p-3 rounded-lg">
                                <span className="block text-gray-400 text-xs uppercase mb-1">Controls Implemented</span>
                                <span className="text-lg font-mono text-emerald-400">{stats.covered}</span>
                            </div>
                            <div className="bg-white/5 p-3 rounded-lg">
                                <span className="block text-gray-400 text-xs uppercase mb-1">Total Controls</span>
                                <span className="text-lg font-mono text-white">{stats.total}</span>
                            </div>
                            <div className="bg-white/5 p-3 rounded-lg flex items-center justify-center group cursor-pointer hover:bg-white/10">
                                <span className="text-sm text-blue-400 flex items-center font-medium">
                                    View Details <ExternalLink size={14} className="ml-2 group-hover:translate-x-1 transition-transform" />
                                </span>
                            </div>
                        </div>
                    </div>
                ))}

                {!coverage && (
                    <div className="text-center py-12 text-gray-500 glass rounded-2xl border border-white/5">
                        Loading compliance data...
                    </div>
                )}
            </div>
        </div>
    );
};

export default Frameworks;
