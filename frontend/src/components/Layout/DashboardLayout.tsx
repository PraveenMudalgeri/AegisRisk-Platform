import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { logout } from '../../store/authSlice';
import {
    LayoutDashboard,
    ShieldAlert,
    Database,
    FileCheck,
    BookOpen,
    Settings,
    LogOut,
    Menu,
    Bell,
    Search
} from 'lucide-react';
import clsx from 'clsx';

const SidebarItem = ({ icon: Icon, label, path, active }: any) => {
    const navigate = useNavigate();
    return (
        <div
            onClick={() => navigate(path)}
            className={clsx(
                "flex items-center space-x-3 px-4 py-3 rounded-xl cursor-pointer transition-all mb-1",
                active ? "bg-primary/10 text-primary border border-primary/20" : "text-gray-400 hover:bg-white/5 hover:text-gray-200"
            )}
        >
            <Icon size={20} />
            <span className="font-medium">{label}</span>
        </div>
    );
};

const DashboardLayout: React.FC = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = () => {
        dispatch(logout());
        navigate('/login');
    };

    const menuItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard' },
        { icon: Database, label: 'Assets', path: '/assets' },
        { icon: ShieldAlert, label: 'Threats', path: '/threats' },
        { icon: FileCheck, label: 'Controls', path: '/controls' },
        { icon: BookOpen, label: 'Frameworks', path: '/frameworks' },
    ];

    return (
        <div className="min-h-screen bg-background flex">
            {/* Sidebar */}
            <div className="w-64 border-r border-white/10 bg-secondary/30 flex-shrink-0 flex flex-col hidden md:flex">
                <div className="p-6">
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                        AegisRisk
                    </h1>
                </div>

                <div className="flex-1 px-4 py-2">
                    <div className="space-y-1">
                        {menuItems.map((item) => (
                            <SidebarItem
                                key={item.path}
                                icon={item.icon}
                                label={item.label}
                                path={item.path}
                                active={location.pathname === item.path}
                            />
                        ))}
                    </div>

                    <div className="mt-8 pt-8 border-t border-white/5">
                        <SidebarItem icon={Settings} label="Settings" path="/settings" />
                    </div>
                </div>

                <div className="p-4 border-t border-white/10">
                    <button
                        onClick={handleLogout}
                        className="flex items-center space-x-3 text-red-400 hover:text-red-300 w-full px-4 py-3 rounded-xl hover:bg-red-500/10 transition-colors"
                    >
                        <LogOut size={20} />
                        <span>Sign Out</span>
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
                {/* Topbar */}
                <header className="h-16 border-b border-white/10 bg-background/80 backdrop-blur-md flex items-center justify-between px-6 z-10 sticky top-0">
                    <div className="flex items-center text-gray-400 md:hidden">
                        <Menu className="h-6 w-6 cursor-pointer" />
                    </div>

                    <div className="hidden md:flex items-center bg-secondary/50 rounded-full px-4 py-2 border border-white/5 w-96">
                        <Search className="h-4 w-4 text-gray-500 mr-2" />
                        <input
                            type="text"
                            placeholder="Search assets, risks, controls..."
                            className="bg-transparent border-none focus:outline-none text-sm text-white w-full placeholder-gray-600"
                        />
                    </div>

                    <div className="flex items-center space-x-4">
                        <div className="h-10 w-10 rounded-full bg-secondary/80 flex items-center justify-center border border-white/10 hover:border-primary/50 cursor-pointer transition-colors relative">
                            <Bell className="h-5 w-5 text-gray-400" />
                            <span className="absolute top-2 right-2 h-2 w-2 bg-red-500 rounded-full"></span>
                        </div>
                        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary to-blue-600 flex items-center justify-center cursor-pointer shadow-lg shadow-primary/20">
                            <span className="font-bold text-white text-sm">JD</span>
                        </div>
                    </div>
                </header>

                {/* Page Content */}
                <main className="flex-1 overflow-y-auto p-6 md:p-8 relative">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default DashboardLayout;
