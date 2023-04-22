import React from 'react';

export interface DupaProps {
    className?: string;
}

export const Dupa: React.FC<DupaProps> = ({ className = '' }) => (
    <>
        <div className={className}>Search</div>
        <input aria-label="dupa"/> 
    </>
    
    
);