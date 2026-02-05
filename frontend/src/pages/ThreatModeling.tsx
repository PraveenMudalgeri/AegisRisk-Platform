import React, { useState } from 'react';
import { ShieldAlert, Zap } from 'lucide-react';

const ThreatModeling: React.FC = () => {
    const [activeTab, setActiveTab] = useState('Spoofing');
    const strideCategories = ['Spoofing', 'Tampering', 'Repudiation', 'Information', 'DoS', 'Elevation'];

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-white">Threat Modeling</h1>
                <p className="text-gray-400">Analyze threats using STRIDE methodology</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-200px)]">
                {/* Sidebar Categories */}
                <div className="lg:col-span-1 glass rounded-2xl p-4 border border-white/10 space-y-2">
                    {strideCategories.map((cat) => (
                        <div
                            key={cat}
                            onClick={() => setActiveTab(cat)}
                            className={`p-3 rounded-xl cursor-pointer transition-all flex items-center justify-between ${activeTab === cat ? 'bg-primary/20 border border-primary/50 text-white' : 'text-gray-400 hover:bg-white/5'}`}
                        >
                            <span className="font-medium">{cat}</span>
                            <span className="text-xs bg-white/10 px-2 py-1 rounded-full">3</span>
                        </div>
                    ))}
                </div>

                {/* Content Area */}
                <div className="lg:col-span-3 glass rounded-2xl p-6 border border-white/10 overflow-y-auto">
                    <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                        <ShieldAlert className="mr-3 text-red-500" />
                        {activeTab} Threats
                    </h2>

                    <div className="space-y-4">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="bg-secondary/40 p-4 rounded-xl border border-white/5 hover:border-white/20 transition-all">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h3 className="text-white font-semibold flex items-center">
                                            <Zap size={16} className="text-amber-500 mr-2" />
                                            Potential Identity Theft via API
                                        </h3>
                                        <p className="text-gray-400 text-sm mt-1">Attackers may attempt to impersonate legitimate users via weak authentication endpoints.</p>
                                    </div>
                                    <span className="bg-red-500/20 text-red-400 text-xs px-2 py-1 rounded font-mono">HIGH</span>
                                </div>
                                <div className="mt-4 flex space-x-3 text-xs text-gray-500">
                                    <div className="flex items-center">
                                        <span className="w-2 h-2 rounded-full bg-indigo-500 mr-2"></span>
                                        Asset: User Service
                                    </div>
                                    <div className="flex items-center">
                                        <span className="w-2 h-2 rounded-full bg-emerald-500 mr-2"></span>
                                        Mitigated: No
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ThreatModeling;
