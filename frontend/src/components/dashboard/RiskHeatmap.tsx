import React from 'react';
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, Cell, CartesianGrid } from 'recharts';

const data = [
    { x: 1, y: 10, z: 20, name: 'Low/High' },
    { x: 5, y: 50, z: 100, name: 'Med/Med' },
    { x: 9, y: 90, z: 200, name: 'High/High' },
    { x: 2, y: 80, z: 50, name: 'Low/High' },
    { x: 8, y: 20, z: 80, name: 'High/Low' },
];

const RiskHeatmap: React.FC = () => {
    return (
        <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
                <ScatterChart
                    margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis type="number" dataKey="x" name="Likelihood" unit="" domain={[0, 10]} stroke="#94a3b8" />
                    <YAxis type="number" dataKey="y" name="Impact" unit="" domain={[0, 100]} stroke="#94a3b8" />
                    <ZAxis type="number" dataKey="z" range={[50, 400]} name="Risk Score" />
                    <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)' }} />
                    <Scatter name="Risks" data={data} fill="#8884d8">
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.y > 50 && entry.x > 5 ? '#ef4444' : entry.y > 50 || entry.x > 5 ? '#f59e0b' : '#10b981'} />
                        ))}
                    </Scatter>
                </ScatterChart>
            </ResponsiveContainer>
        </div>
    );
};

export default RiskHeatmap;
