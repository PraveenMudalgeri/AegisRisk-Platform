import React from 'react';
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Tooltip } from 'recharts';

const data = [
    { subject: 'ISO 27001', A: 65, fullMark: 100 },
    { subject: 'NIST 800-53', A: 48, fullMark: 100 },
    { subject: 'GDPR', A: 80, fullMark: 100 },
    { subject: 'SOC 2', A: 30, fullMark: 100 },
    { subject: 'PCI DSS', A: 55, fullMark: 100 },
];

const ComplianceRadar: React.FC = () => {
    return (
        <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
                    <PolarGrid stroke="rgba(255,255,255,0.1)" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar
                        name="Compliance"
                        dataKey="A"
                        stroke="#00d4ff"
                        strokeWidth={2}
                        fill="#00d4ff"
                        fillOpacity={0.3}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)' }}
                        itemStyle={{ color: '#fff' }}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ComplianceRadar;
