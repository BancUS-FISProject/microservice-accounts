import React from 'react';
import StatusBadge from '../../components/StatusBadge';

const CardList = ({ cards = [] }) => {
    if (!cards || cards.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Tarjetas Asociadas</h3>
                <p className="text-gray-500 text-sm">No hay tarjetas asociadas a esta cuenta</p>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Tarjetas Asociadas</h3>
            <div className="space-y-3">
                {cards.map((card, index) => (
                    <div
                        key={index}
                        className="flex justify-between items-center p-4 bg-gray-50 rounded-lg border border-gray-200"
                    >
                        <div>
                            <p className="font-mono text-sm text-gray-800">
                                **** **** **** {card.numero?.slice(-4) || '****'}
                            </p>
                            <p className="text-xs text-gray-500 mt-1">
                                {card.tipo || 'Débito'} • Vence: {card.fechaVencimiento || 'N/A'}
                            </p>
                        </div>
                        <StatusBadge status={card.estado} />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CardList;
