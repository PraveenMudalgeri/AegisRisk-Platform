import React, { useEffect } from 'react';
import { X, CheckCircle, AlertCircle } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'info';

interface ToastProps {
    message: string;
    type: ToastType;
    onClose: () => void;
}

const Toast: React.FC<ToastProps> = ({ message, type, onClose }) => {
    useEffect(() => {
        const timer = setTimeout(() => {
            onClose();
        }, 5000);
        return () => clearTimeout(timer);
    }, [onClose]);

    const bgColors = {
        success: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400',
        error: 'bg-red-500/10 border-red-500/20 text-red-400',
        info: 'bg-blue-500/10 border-blue-500/20 text-blue-400',
    };

    const icons = {
        success: CheckCircle,
        error: AlertCircle,
        info: AlertCircle,
    };

    const Icon = icons[type];

    return (
        <div className={`fixed bottom-4 right-4 z-50 flex items-center p-4 rounded-xl border backdrop-blur-md shadow-xl min-w-[300px] ${bgColors[type]}`}>
            <Icon size={20} className="mr-3" />
            <span className="flex-1 font-medium text-sm">{message}</span>
            <button onClick={onClose} className="p-1 hover:bg-white/10 rounded-full transition-colors">
                <X size={16} />
            </button>
        </div>
    );
};

export default Toast;
