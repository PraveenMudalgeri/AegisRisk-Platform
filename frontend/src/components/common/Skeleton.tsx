import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
    className?: string;
}

const Skeleton = ({ className, ...props }: SkeletonProps) => {
    return (
        <div
            className={twMerge(clsx("animate-pulse rounded-md bg-white/10", className))}
            {...props}
        />
    );
};

export default Skeleton;
