import React from 'react';
import { AlertTriangle, ChevronRight } from 'lucide-react';

const risks = [
    { id: 1, title: 'Unpatched SQL Server', asset: 'Customer DB', score: 85, ale: '$250k' },
    { id: 2, title: 'Weak Password Policy', asset: 'Internal IAM', score: 72, ale: '$120k' },
    { id: 3, title: 'Open S3 Bucket', asset: 'Backup Storage', score: 68, ale: '$90k' },
    { id: 4, title: 'No MFA on Admin', asset: 'AWS Root', score: 95, ale: '$500k' },
    { id: 5, title: 'Legacy Protocol', asset: 'VPN Gateway', score: 60, ale: '$50k' },
];

const TopCriticalRisks: React.FC = () => {
    return (
        <div className="glass rounded-2xl p-6 border border-white/10 h-full">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-white">Top Critical Risks</h3>
                <button className="text-xs text-primary hover:text-cyan-300 transition-colors">View All</button>
            </div>

            <div className="space-y-3">
                {risks.sort((a, b) => b.score - a.score).slice(0, 5).map((risk) => (
                    <div key={risk.id} className="group flex items-center p-3 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 hover:border-white/10 transition-all cursor-pointer">
                        <div className={`h-10 w-10 rounded-lg flex items-center justify-center mr-4 ${risk.score >= 80 ? 'bg-red-500/20 text-red-500' : 'bg-amber-500/20 text-amber-500'}`}>
                            <AlertTriangle size={20} />
                        </div>

                        <div className="flex-1 min-w-0">
                            <h4 className="text-sm font-medium text-white truncate group-hover:text-primary transition-colors">{risk.title}</h4>
                            <p className="text-xs text-gray-500 truncate">{risk.asset}</p>
                        </div>

                        <div className="text-right mx-4">
                            <div className="text-sm font-bold text-gray-200">{risk.score}</div>
                            <div className="text-xs text-gray-500">Score</div>
                        </div>

                        <ChevronRight size={16} className="text-gray-600 group-hover:text-white transition-colors" />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TopCriticalRisks;
