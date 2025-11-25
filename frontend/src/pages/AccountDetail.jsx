import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import AccountCard from '../features/accounts/AccountCard';
import TransactionForm from '../features/accounts/TransactionForm';
import CardList from '../features/accounts/CardList';
import Button from '../components/Button';

const AccountDetail = () => {
    const { iban } = useParams();
    const navigate = useNavigate();
    const [account, setAccount] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        // Aquí se llamará al servicio para obtener los datos de la cuenta
        // Por ahora, datos de ejemplo
        const fetchAccount = async () => {
            try {
                setLoading(true);
                // Simulación de llamada a API
                // const data = await accountService.getAccountByIban(iban);

                // Datos de ejemplo
                const mockData = {
                    iban: iban,
                    saldo: 1500.50,
                    estado: 'Activa',
                    titular: 'Juan Pérez García',
                    blocked: false, // Estado de bloqueo de la cuenta
                    tarjetas: [
                        {
                            numero: '1234567890123456',
                            tipo: 'Débito',
                            fechaVencimiento: '12/25',
                            estado: 'Activa'
                        }
                    ]
                };

                setAccount(mockData);
            } catch (err) {
                setError('Error al cargar la cuenta');
            } finally {
                setLoading(false);
            }
        };

        fetchAccount();
    }, [iban]);

    const handleTransaction = async (transaction) => {
        try {
            // Aquí se llamará al servicio para realizar la transacción
            // await accountService.performTransaction(iban, transaction);

            // Actualizar saldo localmente (temporal)
            setAccount(prev => ({
                ...prev,
                saldo: transaction.type === 'depositar'
                    ? prev.saldo + transaction.amount
                    : prev.saldo - transaction.amount
            }));

            alert(`${transaction.type === 'depositar' ? 'Depósito' : 'Retiro'} realizado con éxito`);
        } catch (err) {
            alert('Error al realizar la transacción');
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
                <p className="text-gray-600">Cargando...</p>
            </div>
        );
    }

    if (error || !account) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
                <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full text-center">
                    <p className="text-red-600 mb-4">{error || 'Cuenta no encontrada'}</p>
                    <Button onClick={() => navigate('/')} variant="primary">
                        Volver al inicio
                    </Button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 py-8">
            <div className="max-w-6xl mx-auto">
                <div className="mb-6">
                    <Button onClick={() => navigate('/')} variant="secondary">
                        ← Volver
                    </Button>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2 space-y-6">
                        <AccountCard account={account} />
                        <CardList cards={account.tarjetas} />
                    </div>

                    <div>
                        <TransactionForm
                            onSubmit={handleTransaction}
                            accountBalance={account.saldo}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AccountDetail;
