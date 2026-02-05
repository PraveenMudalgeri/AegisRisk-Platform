import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Assets from './pages/Assets';
import ThreatModeling from './pages/ThreatModeling';
import Controls from './pages/Controls';
import Frameworks from './pages/Frameworks';
import Reports from './pages/Reports';
import DashboardLayout from './components/Layout/DashboardLayout';
import { useSelector } from 'react-redux';
import { RootState } from './store';

const PrivateRoute = ({ children }: { children: JSX.Element }) => {
    const { isAuthenticated } = useSelector((state: RootState) => state.auth);
    return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />

                <Route path="/" element={<PrivateRoute><DashboardLayout /></PrivateRoute>}>
                    <Route index element={<Navigate to="/dashboard" replace />} />
                    <Route path="dashboard" element={<Dashboard />} />
                    <Route path="assets" element={<Assets />} />
                    <Route path="threats" element={<ThreatModeling />} />
                    <Route path="controls" element={<Controls />} />
                    <Route path="frameworks" element={<Frameworks />} />
                    <Route path="reports" element={<Reports />} />
                    <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Route>
            </Routes>
        </Router>
    );
}

export default App;
