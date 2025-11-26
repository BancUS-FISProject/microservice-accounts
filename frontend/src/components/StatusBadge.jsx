import React from 'react';

const StatusBadge = ({ status }) => {
    const isActive = status === 'Activa' || status === 'ACTIVE';

    const styles = isActive
        ? 'bg-green-100 text-green-800 border-green-300'
        : 'bg-red-100 text-red-800 border-red-300';

    const displayText = isActive ? 'Activa' : 'Bloqueada';

    return (
        <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${styles}`}>
            {displayText}
        </span>
    );
};

export default StatusBadge;
