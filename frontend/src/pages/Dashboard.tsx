import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { fetchRiskStats } from '../store/slices/risksSlice';
import { fetchAssets } from '../store/slices/assetsSlice';
import { fetchControls } from '../store/slices/controlsSlice';
import { Activity, ShieldCheck, AlertTriangle, Target } from 'lucide-react';
import OrgRiskScoreCard from '../components/dashboard/OrgRiskScoreCard';
import RiskHeatmap from '../components/dashboard/RiskHeatmap';
import ComplianceRadar from '../components/dashboard/ComplianceRadar';
import TopCriticalRisks from '../components/dashboard/TopCriticalRisks';
import STRIDEDistribution from '../components/dashboard/STRIDEDistribution';
import Skeleton from '../components/common/Skeleton';

const StatCard = ({ title, value, change, icon: Icon, color, loading }: any) => {
    if (loading) return <Skeleton className="h-40 w-full rounded-2xl" />;

    return (
        <div className="glass p-6 rounded-2xl relative overflow-hidden group hover:border-white/20 transition-all">
            <div className={`absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity ${color}`}>
                <Icon size={64} />
            </div>
            <div className="flex items-center space-x-4">
                <div className={`p-3 rounded-xl ${color} bg-opacity-10 text-white border border-white/10`}>
                    <Icon size={24} />
                </div>
                <div>
                    <p className="text-gray-400 text-sm font-medium">{title}</p>
                    <h3 className="text-2xl font-bold text-white mt-1">{value}</h3>
                </div>
            </div>
            <div className="mt-4 flex items-center text-sm">
                <span className="text-emerald-400 font-medium">{change}</span>
                <span className="text-gray-500 ml-2">vs last month</span>
            </div>
        </div>
    );
};

const Dashboard: React.FC = () => {
    const dispatch = useDispatch<AppDispatch>();
    const { stats, loading } = useSelector((state: RootState) => state.risks);
    const { items: assets } = useSelector((state: RootState) => state.assets);
    const { items: controls } = useSelector((state: RootState) => state.controls);

    useEffect(() => {
        dispatch(fetchRiskStats());
        dispatch(fetchAssets());
        dispatch(fetchControls());
    }, [dispatch]);

    // Calculate derived stats
    const activeThreats = Object.values(stats?.severity_counts || {}).reduce((a, b) => a + b, 0);
    const implementedControls = controls.filter(c => c.implementation_status === 'IMPLEMENTED').length;
    const controlCoverage = controls.length ? Math.round((implementedControls / controls.length) * 100) : 0;

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-white">Security Overview</h1>
                <p className="text-gray-400 mt-1">Real-time risk posture and compliance status</p>
            </div>

            {/* Top Stats Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {loading ? (
                    <Skeleton className="h-40 w-full rounded-2xl" />
                ) : (
                    <OrgRiskScoreCard score={stats?.overall_score_avg || 0} />
                )}

                <StatCard
                    title="Active Threats"
                    value={activeThreats}
                    change="+2"
                    icon={AlertTriangle}
                    color="bg-red-500"
                    loading={loading}
                />
                <StatCard
                    title="Control Coverage"
                    value={`${controlCoverage}%`}
                    change={`+${controlCoverage > 10 ? 5 : 0}%`}
                    icon={ShieldCheck}
                    color="bg-emerald-500"
                    loading={loading}
                />
                <StatCard
                    title="Total Assets"
                    value={assets.length}
                    change="+1"
                    icon={Target}
                    color="bg-purple-500"
                    loading={loading}
                />
            </div>

            {/* Charts Row 1 */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 glass rounded-2xl p-6 border border-white/10">
                    <h3 className="text-lg font-semibold text-white mb-6">Risk Heatmap (Likelihood vs Impact)</h3>
                    {loading ? <Skeleton className="h-64 w-full rounded-2xl" /> : <RiskHeatmap />}
                </div>
                <div className="glass rounded-2xl p-6 border border-white/10">
                    <h3 className="text-lg font-semibold text-white mb-6">Compliance Coverage</h3>
                    {loading ? <Skeleton className="h-64 w-full rounded-2xl" /> : <ComplianceRadar />}
                </div>
            </div>

            {/* Charts Row 2 */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1">
                    <TopCriticalRisks />
                </div>
                <div className="lg:col-span-2 glass rounded-2xl p-6 border border-white/10">
                    <h3 className="text-lg font-semibold text-white mb-6">Threat Distribution (STRIDE)</h3>
                    <STRIDEDistribution />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
