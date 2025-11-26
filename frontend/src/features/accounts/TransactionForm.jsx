import React, { useState } from 'react';
import Input from '../../components/Input';
import Button from '../../components/Button';

const TransactionForm = ({ onSubmit, accountBalance }) => {
    const [transactionType, setTransactionType] = useState('depositar');
    const [amount, setAmount] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        const numAmount = parseFloat(amount);

        if (!amount || numAmount <= 0) {
            setError('Ingrese un monto válido mayor a 0');
            return;
        }

        if (transactionType === 'retirar' && numAmount > accountBalance) {
            setError('Saldo insuficiente para realizar el retiro');
            return;
        }

        onSubmit({
            type: transactionType,
            amount: numAmount
        });

        setAmount('');
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Nueva Operación</h3>

            <div className="mb-4">
                <label className="text-sm font-medium text-gray-700 mb-2 block">Tipo de operación</label>
                <div className="flex gap-4">
                    <label className="flex items-center cursor-pointer">
                        <input
                            type="radio"
                            value="depositar"
                            checked={transactionType === 'depositar'}
                            onChange={(e) => setTransactionType(e.target.value)}
                            className="mr-2"
                        />
                        <span className="text-sm">Depositar</span>
                    </label>
                    <label className="flex items-center cursor-pointer">
                        <input
                            type="radio"
                            value="retirar"
                            checked={transactionType === 'retirar'}
                            onChange={(e) => setTransactionType(e.target.value)}
                            className="mr-2"
                        />
                        <span className="text-sm">Retirar</span>
                    </label>
                </div>
            </div>

            <Input
                label="Monto"
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                required
                error={error}
                className="mb-4"
            />

            <Button
                type="submit"
                variant={transactionType === 'depositar' ? 'success' : 'danger'}
                className="w-full"
            >
                {transactionType === 'depositar' ? 'Depositar' : 'Retirar'}
            </Button>
        </form>
    );
};

export default TransactionForm;
