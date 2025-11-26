import React from 'react';
import StatusBadge from '../../components/StatusBadge';

const AccountCard = ({ account, onClick }) => {
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'EUR'
        }).format(amount);
    };

    const formatCardNumber = (cardNumber) => {
        if (!cardNumber) return 'N/A';
        return cardNumber;
    };

    return (
        <div
            onClick={onClick}
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer border border-gray-200"
        >
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-lg font-semibold text-gray-800">Cuenta Bancaria</h3>
                    <p className="text-sm text-gray-500 font-mono mt-1">{account.iban}</p>
                </div>
                <StatusBadge status={account.estado} />
            </div>

            <div className="mt-4">
                <p className="text-sm text-gray-600">Saldo disponible</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">
                    {formatCurrency(account.saldo)}
                </p>
            </div>

            {account.titular && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                    <p className="text-sm text-gray-600">Titular</p>
                    <p className="text-sm font-medium text-gray-800">{account.titular}</p>
                </div>
            )}

            {/* Estado de bloqueo */}
            <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-sm text-gray-600">Estado de bloqueo</p>
                <div className="flex items-center mt-1">
                    {account.blocked ? (
                        <span className="flex items-center text-sm font-medium text-red-600">
                            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M13.477 14.89A6 6 0 015.11 6.524l8.367 8.368zm1.414-1.414L6.524 5.11a6 6 0 018.367 8.367zM18 10a8 8 0 11-16 0 8 8 0 0116 0z" clipRule="evenodd" />
                            </svg>
                            Cuenta bloqueada
                        </span>
                    ) : (
                        <span className="flex items-center text-sm font-medium text-green-600">
                            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            Cuenta activa
                        </span>
                    )}
                </div>
            </div>

            {account.cards && account.cards.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                    <p className="text-sm text-gray-600">Tarjeta principal</p>
                    <p className="text-sm font-mono font-medium text-gray-800 mt-1">
                        {account.cards[0]}
                    </p>
                </div>
            )}
        </div>
    );
};

export default AccountCard;
