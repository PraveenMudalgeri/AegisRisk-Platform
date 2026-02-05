import React from 'react';
import { Activity, TrendingDown } from 'lucide-react';

interface Props {
    score: number;
    trend?: number;
}

const OrgRiskScoreCard: React.FC<Props> = ({ score }) => {
    // Determine color based on score
    const getColor = (s: number) => {
        if (s < 20) return 'text-emerald-500';
        if (s < 50) return 'text-amber-500';
        return 'text-red-500';
    };

    return (
        <div className="glass p-6 rounded-2xl relative overflow-hidden flex flex-col justify-between h-full group hover:border-primary/30 transition-all">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity bg-primary rounded-bl-3xl">
                <Activity size={80} className="text-white" />
            </div>

            <div>
                <h3 className="text-gray-400 font-medium mb-1">Organization Risk Score</h3>
                <p className="text-xs text-gray-500">Aggregated FAIR Analysis</p>
            </div>

            <div className="mt-6 flex items-end space-x-4">
                <span className={`text-6xl font-bold ${getColor(score)}`}>
                    {score.toFixed(1)}
                </span>
                <div className="pb-2">
                    <span className="flex items-center text-emerald-400 text-sm font-medium bg-emerald-400/10 px-2 py-1 rounded">
                        <TrendingDown size={14} className="mr-1" />
                        5.2%
                    </span>
                </div>
            </div>

            <div className="mt-4 w-full h-2 bg-gray-700/50 rounded-full overflow-hidden">
                <div
                    className="h-full bg-gradient-to-r from-emerald-500 via-amber-500 to-red-500"
                    style={{ width: `${Math.min(score, 100)}%` }}
                ></div>
            </div>
        </div>
    );
};

export default OrgRiskScoreCard;
