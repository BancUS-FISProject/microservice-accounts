import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Input from '../components/Input';
import Button from '../components/Button';

const HomePage = () => {
    const [iban, setIban] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSearch = (e) => {
        e.preventDefault();
        setError('');

        if (!iban.trim()) {
            setError('Por favor ingrese un IBAN');
            return;
        }

        // Navegar a la página de detalle de cuenta
        navigate(`/account/${iban}`);
    };

    const handleCreateAccount = () => {
        // Navegar a formulario de creación de cuenta
        navigate('/account/create');
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
            <div className="max-w-md w-full">
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold text-gray-800 mb-2">Gestión de Cuentas</h1>
                    <p className="text-gray-600">Busca una cuenta o crea una nueva</p>
                </div>

                <div className="bg-white rounded-lg shadow-xl p-8 border border-gray-200">
                    <form onSubmit={handleSearch} className="mb-6">
                        <Input
                            label="Buscar cuenta por IBAN"
                            type="text"
                            value={iban}
                            onChange={(e) => setIban(e.target.value)}
                            placeholder="ES91 2100 0418 4502 0005 1332"
                            error={error}
                            className="mb-4"
                        />
                        <Button type="submit" variant="primary" className="w-full">
                            Buscar Cuenta
                        </Button>
                    </form>

                    <div className="relative my-6">
                        <div className="absolute inset-0 flex items-center">
                            <div className="w-full border-t border-gray-300"></div>
                        </div>
                        <div className="relative flex justify-center text-sm">
                            <span className="px-2 bg-white text-gray-500">o</span>
                        </div>
                    </div>

                    <Button
                        onClick={handleCreateAccount}
                        variant="secondary"
                        className="w-full"
                    >
                        Crear Nueva Cuenta
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default HomePage;
