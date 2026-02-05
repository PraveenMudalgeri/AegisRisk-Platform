import React, { useState } from 'react';
import api from '../services/api';
import { FileText, Download, CheckCircle } from 'lucide-react';

interface ReportData {
    title: string;
    generated_at: string;
    [key: string]: any;
}

const Reports: React.FC = () => {
    const [reportType, setReportType] = useState('risk_summary');
    const [data, setData] = useState<ReportData | null>(null);
    const [loading, setLoading] = useState(false);

    const generateReport = async () => {
        setLoading(true);
        try {
            const response = await api.post(`/reports/generate?report_type=${reportType}`);
            setData(response.data);
        } catch (e) {
            console.error(e);
            alert('Failed to generate report');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-white">Reports Center</h1>
                <p className="text-gray-400">Generate executive summaries and compliance artifacts</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Configuration Panel */}
                <div className="glass p-6 rounded-2xl border border-white/10 h-fit">
                    <h3 className="text-lg font-semibold text-white mb-4">Report Configuration</h3>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">Report Type</label>
                            <select
                                value={reportType}
                                onChange={(e) => setReportType(e.target.value)}
                                className="w-full bg-secondary/50 border border-white/10 rounded-xl px-4 py-2 text-white focus:outline-none focus:border-primary"
                            >
                                <option value="risk_summary">Executive Risk Summary</option>
                                <option value="compliance">Compliance Status Report</option>
                            </select>
                        </div>

                        <button
                            onClick={generateReport}
                            disabled={loading}
                            className="w-full bg-primary hover:bg-cyan-400 text-white font-bold py-3 px-4 rounded-xl transition-all shadow-lg shadow-primary/20 disabled:opacity-50"
                        >
                            {loading ? 'Generating...' : 'Generate Report'}
                        </button>
                    </div>
                </div>

                {/* Preview Panel */}
                <div className="lg:col-span-2 glass p-6 rounded-2xl border border-white/10 min-h-[400px]">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-lg font-semibold text-white">Report Preview</h3>
                        {data && (
                            <div className="flex space-x-2">
                                <button className="flex items-center px-3 py-1.5 bg-white/5 hover:bg-white/10 rounded-lg text-sm text-gray-300 transition-colors">
                                    <Download size={16} className="mr-2" /> PDF
                                </button>
                                <button className="flex items-center px-3 py-1.5 bg-white/5 hover:bg-white/10 rounded-lg text-sm text-gray-300 transition-colors">
                                    <FileText size={16} className="mr-2" /> Excel
                                </button>
                            </div>
                        )}
                    </div>

                    {data ? (
                        <div className="bg-black/30 p-6 rounded-xl border border-white/5 font-mono text-sm overflow-auto">
                            <h2 className="text-xl font-bold text-white mb-2">{data.title}</h2>
                            <p className="text-gray-500 mb-6">Generated: {new Date(data.generated_at).toLocaleString()}</p>

                            <pre className="text-green-400 whitespace-pre-wrap">
                                {JSON.stringify(data, null, 2)}
                            </pre>
                        </div>
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center text-gray-500 border-2 border-dashed border-white/5 rounded-xl">
                            <FileText size={48} className="mb-4 opacity-20" />
                            <p>Select a report type and click Generate</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Reports;
