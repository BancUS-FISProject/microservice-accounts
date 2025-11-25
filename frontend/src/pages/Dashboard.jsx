import React, { useState } from 'react';
import accountService from '../services/accountService';

const Dashboard = () => {
    const [currentAccount, setCurrentAccount] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });

    // Form states
    const [iban, setIban] = useState('');
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [subscription, setSubscription] = useState('Free');
    const [balance, setBalance] = useState('');
    const [pan, setPan] = useState('');

    const showMessage = (type, text) => {
        setMessage({ type, text });
        setTimeout(() => setMessage({ type: '', text: '' }), 5000);
    };

    // 1. Crear cuenta
    const handleCreateAccount = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const result = await accountService.createAccount({ name, email, subscription });
            setCurrentAccount(result);
            showMessage('success', `Cuenta creada exitosamente. IBAN: ${result.iban}`);
            setName('');
            setEmail('');
            setSubscription('Free');
        } catch (error) {
            showMessage('danger', `Error al crear cuenta: ${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // 2. Obtener cuenta por IBAN
    const handleGetAccount = async (e) => {
        e.preventDefault();
        if (!iban.trim()) {
            showMessage('warning', 'Por favor ingrese un IBAN');
            return;
        }
        setLoading(true);
        try {
            const result = await accountService.getAccountByIban(iban);
            setCurrentAccount(result);
            showMessage('success', 'Cuenta cargada exitosamente');
        } catch (error) {
            showMessage('danger', `Error al obtener cuenta: ${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // 3. Actualizar información de cuenta
    const handleUpdateAccount = async (e) => {
        e.preventDefault();
        if (!currentAccount) {
            showMessage('warning', 'Primero debe cargar una cuenta');
            return;
        }
        setLoading(true);
        try {
            const updateData = {};
            if (name) updateData.name = name;
            if (email) updateData.email = email;
            if (subscription) updateData.subscription = subscription;

            const result = await accountService.updateAccount(currentAccount.iban, updateData);
            setCurrentAccount(result);
            showMessage('success', 'Cuenta actualizada exitosamente');
            setName('');
            setEmail('');
        } catch (error) {
            showMessage('danger', `Error al actualizar cuenta: ${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // 4. Actualizar balance (depositar/retirar)
    const handleUpdateBalance = async (e, isDeposit) => {
        e.preventDefault();
        if (!currentAccount) {
            showMessage('warning', 'Primero debe cargar una cuenta');
            return;
        }
        if (!balance || parseFloat(balance) <= 0) {
            showMessage('warning', 'Ingrese un monto válido');
            return;
        }
        setLoading(true);
        try {
            const amount = parseFloat(balance);
            const result = isDeposit
                ? await accountService.deposit(currentAccount.iban, amount)
                : await accountService.withdraw(currentAccount.iban, amount);
            setCurrentAccount(result);
            showMessage('success', `${isDeposit ? 'Depósito' : 'Retiro'} realizado exitosamente`);
            setBalance('');
        } catch (error) {
            showMessage('danger', `Error al actualizar balance: ${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // 5. Crear tarjeta
    const handleCreateCard = async () => {
        if (!currentAccount) {
            showMessage('warning', 'Primero debe cargar una cuenta');
            return;
        }
        setLoading(true);
        try {
            const result = await accountService.createCard(currentAccount.iban);
            setCurrentAccount(result);
            showMessage('success', 'Tarjeta creada exitosamente');
        } catch (error) {
            showMessage('danger', `Error al crear tarjeta: ${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // 6. Eliminar tarjeta
    const handleDeleteCard = async (e) => {
        e.preventDefault();
        if (!currentAccount) {
            showMessage('warning', 'Primero debe cargar una cuenta');
            return;
        }
        if (!pan.trim()) {
            showMessage('warning', 'Ingrese el número de tarjeta (PAN)');
            return;
        }
        setLoading(true);
        try {
            await accountService.deleteCard(currentAccount.iban, pan);
            const updatedAccount = await accountService.getAccountByIban(currentAccount.iban);
            setCurrentAccount(updatedAccount);
            showMessage('success', 'Tarjeta eliminada exitosamente');
            setPan('');
        } catch (error) {
            showMessage('danger', `Error al eliminar tarjeta: ${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // 7. Bloquear cuenta
    const handleBlockAccount = async () => {
        if (!currentAccount) {
            showMessage('warning', 'Primero debe cargar una cuenta');
            return;
        }
        setLoading(true);
        try {
            const result = await accountService.blockAccount(currentAccount.iban);
            setCurrentAccount(result);
            showMessage('success', 'Cuenta bloqueada exitosamente');
        } catch (error) {
            showMessage('danger', `Error al bloquear cuenta: ${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // 8. Desbloquear cuenta
    const handleUnblockAccount = async () => {
        if (!currentAccount) {
            showMessage('warning', 'Primero debe cargar una cuenta');
            return;
        }
        setLoading(true);
        try {
            const result = await accountService.unblockAccount(currentAccount.iban);
            setCurrentAccount(result);
            showMessage('success', 'Cuenta desbloqueada exitosamente');
        } catch (error) {
            showMessage('danger', `Error al desbloquear cuenta: ${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // 9. Eliminar cuenta
    const handleDeleteAccount = async () => {
        if (!currentAccount) {
            showMessage('warning', 'Primero debe cargar una cuenta');
            return;
        }
        if (!window.confirm('¿Está seguro de que desea eliminar esta cuenta? Esta acción no se puede deshacer.')) {
            return;
        }
        setLoading(true);
        try {
            await accountService.deleteAccount(currentAccount.iban);
            setCurrentAccount(null);
            showMessage('success', 'Cuenta eliminada exitosamente');
        } catch (error) {
            showMessage('danger', `Error al eliminar cuenta: ${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container-fluid py-4" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
            <div className="row">
                <div className="col-12 mb-4">
                    <h1 className="text-center mb-3">Panel de Gestión de Cuentas</h1>
                    {message.text && (
                        <div className={`alert alert-${message.type} alert-dismissible fade show`} role="alert">
                            {message.text}
                            <button type="button" className="btn-close" onClick={() => setMessage({ type: '', text: '' })}></button>
                        </div>
                    )}
                </div>

                {/* Columna izquierda - Operaciones */}
                <div className="col-lg-8">
                    <div className="card shadow-sm mb-4">
                        <div className="card-header bg-primary text-white">
                            <h5 className="mb-0">Operaciones de API</h5>
                        </div>
                        <div className="card-body">
                            {/* Acordeón de operaciones */}
                            <div className="accordion" id="operationsAccordion">

                                {/* 1. Crear Cuenta */}
                                <div className="accordion-item">
                                    <h2 className="accordion-header">
                                        <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#createAccount">
                                            1. Crear Nueva Cuenta
                                        </button>
                                    </h2>
                                    <div id="createAccount" className="accordion-collapse collapse show" data-bs-parent="#operationsAccordion">
                                        <div className="accordion-body">
                                            <form onSubmit={handleCreateAccount}>
                                                <div className="mb-3">
                                                    <label className="form-label">Nombre</label>
                                                    <input type="text" className="form-control" value={name} onChange={(e) => setName(e.target.value)} required />
                                                </div>
                                                <div className="mb-3">
                                                    <label className="form-label">Email</label>
                                                    <input type="email" className="form-control" value={email} onChange={(e) => setEmail(e.target.value)} required />
                                                </div>
                                                <div className="mb-3">
                                                    <label className="form-label">Suscripción</label>
                                                    <select className="form-select" value={subscription} onChange={(e) => setSubscription(e.target.value)}>
                                                        <option value="Free">Free</option>
                                                        <option value="Premium">Premium</option>
                                                        <option value="Gold">Gold</option>
                                                    </select>
                                                </div>
                                                <button type="submit" className="btn btn-success" disabled={loading}>
                                                    {loading ? 'Creando...' : 'Crear Cuenta'}
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </div>

                                {/* 2. Obtener Cuenta */}
                                <div className="accordion-item">
                                    <h2 className="accordion-header">
                                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#getAccount">
                                            2. Buscar Cuenta por IBAN
                                        </button>
                                    </h2>
                                    <div id="getAccount" className="accordion-collapse collapse" data-bs-parent="#operationsAccordion">
                                        <div className="accordion-body">
                                            <form onSubmit={handleGetAccount}>
                                                <div className="mb-3">
                                                    <label className="form-label">IBAN</label>
                                                    <input type="text" className="form-control" value={iban} onChange={(e) => setIban(e.target.value)} placeholder="ES91 2100 0418 4502 0005 1332" required />
                                                </div>
                                                <button type="submit" className="btn btn-primary" disabled={loading}>
                                                    {loading ? 'Buscando...' : 'Buscar Cuenta'}
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </div>

                                {/* 3. Actualizar Cuenta */}
                                <div className="accordion-item">
                                    <h2 className="accordion-header">
                                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#updateAccount">
                                            3. Actualizar Información de Cuenta
                                        </button>
                                    </h2>
                                    <div id="updateAccount" className="accordion-collapse collapse" data-bs-parent="#operationsAccordion">
                                        <div className="accordion-body">
                                            <form onSubmit={handleUpdateAccount}>
                                                <div className="mb-3">
                                                    <label className="form-label">Nuevo Nombre (opcional)</label>
                                                    <input type="text" className="form-control" value={name} onChange={(e) => setName(e.target.value)} />
                                                </div>
                                                <div className="mb-3">
                                                    <label className="form-label">Nuevo Email (opcional)</label>
                                                    <input type="email" className="form-control" value={email} onChange={(e) => setEmail(e.target.value)} />
                                                </div>
                                                <div className="mb-3">
                                                    <label className="form-label">Nueva Suscripción (opcional)</label>
                                                    <select className="form-select" value={subscription} onChange={(e) => setSubscription(e.target.value)}>
                                                        <option value="Free">Free</option>
                                                        <option value="Premium">Premium</option>
                                                        <option value="Gold">Gold</option>
                                                    </select>
                                                </div>
                                                <button type="submit" className="btn btn-warning" disabled={loading || !currentAccount}>
                                                    {loading ? 'Actualizando...' : 'Actualizar Cuenta'}
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </div>

                                {/* 4. Depositar/Retirar */}
                                <div className="accordion-item">
                                    <h2 className="accordion-header">
                                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#balance">
                                            4. Depositar / Retirar Dinero
                                        </button>
                                    </h2>
                                    <div id="balance" className="accordion-collapse collapse" data-bs-parent="#operationsAccordion">
                                        <div className="accordion-body">
                                            <div className="mb-3">
                                                <label className="form-label">Monto</label>
                                                <input type="number" step="0.01" className="form-control" value={balance} onChange={(e) => setBalance(e.target.value)} placeholder="0.00" />
                                            </div>
                                            <div className="btn-group" role="group">
                                                <button type="button" className="btn btn-success" onClick={(e) => handleUpdateBalance(e, true)} disabled={loading || !currentAccount}>
                                                    Depositar
                                                </button>
                                                <button type="button" className="btn btn-danger" onClick={(e) => handleUpdateBalance(e, false)} disabled={loading || !currentAccount}>
                                                    Retirar
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* 5. Crear Tarjeta */}
                                <div className="accordion-item">
                                    <h2 className="accordion-header">
                                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#createCard">
                                            5. Crear Nueva Tarjeta
                                        </button>
                                    </h2>
                                    <div id="createCard" className="accordion-collapse collapse" data-bs-parent="#operationsAccordion">
                                        <div className="accordion-body">
                                            <p className="text-muted">Crea una nueva tarjeta asociada a la cuenta actual.</p>
                                            <button type="button" className="btn btn-info" onClick={handleCreateCard} disabled={loading || !currentAccount}>
                                                {loading ? 'Creando...' : 'Crear Tarjeta'}
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                {/* 6. Eliminar Tarjeta */}
                                <div className="accordion-item">
                                    <h2 className="accordion-header">
                                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#deleteCard">
                                            6. Eliminar Tarjeta
                                        </button>
                                    </h2>
                                    <div id="deleteCard" className="accordion-collapse collapse" data-bs-parent="#operationsAccordion">
                                        <div className="accordion-body">
                                            <form onSubmit={handleDeleteCard}>
                                                <div className="mb-3">
                                                    <label className="form-label">Número de Tarjeta (PAN)</label>
                                                    <input type="text" className="form-control" value={pan} onChange={(e) => setPan(e.target.value)} placeholder="1234567890123456" required />
                                                </div>
                                                <button type="submit" className="btn btn-danger" disabled={loading || !currentAccount}>
                                                    {loading ? 'Eliminando...' : 'Eliminar Tarjeta'}
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </div>

                                {/* 7. Bloquear/Desbloquear Cuenta */}
                                <div className="accordion-item">
                                    <h2 className="accordion-header">
                                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#blockAccount">
                                            7. Bloquear / Desbloquear Cuenta
                                        </button>
                                    </h2>
                                    <div id="blockAccount" className="accordion-collapse collapse" data-bs-parent="#operationsAccordion">
                                        <div className="accordion-body">
                                            <div className="btn-group" role="group">
                                                <button type="button" className="btn btn-warning" onClick={handleBlockAccount} disabled={loading || !currentAccount}>
                                                    Bloquear Cuenta
                                                </button>
                                                <button type="button" className="btn btn-success" onClick={handleUnblockAccount} disabled={loading || !currentAccount}>
                                                    Desbloquear Cuenta
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* 8. Eliminar Cuenta */}
                                <div className="accordion-item">
                                    <h2 className="accordion-header">
                                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#deleteAccount">
                                            8. Eliminar Cuenta
                                        </button>
                                    </h2>
                                    <div id="deleteAccount" className="accordion-collapse collapse" data-bs-parent="#operationsAccordion">
                                        <div className="accordion-body">
                                            <p className="text-danger">⚠️ Esta acción es irreversible. La cuenta será eliminada permanentemente.</p>
                                            <button type="button" className="btn btn-danger" onClick={handleDeleteAccount} disabled={loading || !currentAccount}>
                                                {loading ? 'Eliminando...' : 'Eliminar Cuenta'}
                                            </button>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>

                {/* Columna derecha - Vista de Cuenta */}
                <div className="col-lg-4">
                    <div className="card shadow-sm sticky-top" style={{ top: '20px' }}>
                        <div className="card-header bg-success text-white">
                            <h5 className="mb-0">Vista de Cuenta</h5>
                        </div>
                        <div className="card-body">
                            {currentAccount ? (
                                <div>
                                    <div className="mb-3">
                                        <h6 className="text-muted mb-1">IBAN</h6>
                                        <p className="font-monospace">{currentAccount.iban}</p>
                                    </div>
                                    <div className="mb-3">
                                        <h6 className="text-muted mb-1">Titular</h6>
                                        <p>{currentAccount.name}</p>
                                    </div>
                                    <div className="mb-3">
                                        <h6 className="text-muted mb-1">Email</h6>
                                        <p>{currentAccount.email}</p>
                                    </div>
                                    <div className="mb-3">
                                        <h6 className="text-muted mb-1">Suscripción</h6>
                                        <span className="badge bg-info">{currentAccount.subscription}</span>
                                    </div>
                                    <div className="mb-3">
                                        <h6 className="text-muted mb-1">Balance</h6>
                                        <h3 className="text-success">${currentAccount.balance?.toFixed(2) || '0.00'}</h3>
                                    </div>
                                    <div className="mb-3">
                                        <h6 className="text-muted mb-1">Estado</h6>
                                        <span className={`badge ${currentAccount.status === 'Active' ? 'bg-success' : 'bg-danger'}`}>
                                            {currentAccount.status}
                                        </span>
                                    </div>

                                    {/* Estado de bloqueo */}
                                    <div className="mb-3">
                                        <h6 className="text-muted mb-1">Estado de bloqueo</h6>
                                        {currentAccount.blocked ? (
                                            <span className="badge bg-danger">
                                                🔒 Cuenta bloqueada
                                            </span>
                                        ) : (
                                            <span className="badge bg-success">
                                                ✓ Cuenta activa
                                            </span>
                                        )}
                                    </div>

                                    {/* Número de tarjeta principal */}
                                    {currentAccount.cards && currentAccount.cards.length > 0 && (
                                        <div className="mb-3">
                                            <h6 className="text-muted mb-1">Tarjeta principal</h6>
                                            <p className="font-monospace">**** **** **** {currentAccount.cards[0].pan?.slice(-4) || '****'}</p>
                                        </div>
                                    )}

                                    {/* Tarjetas */}
                                    {currentAccount.cards && currentAccount.cards.length > 0 && (
                                        <div className="mt-4">
                                            <h6 className="text-muted mb-2">Tarjetas Asociadas</h6>
                                            <div className="list-group">
                                                {currentAccount.cards.map((card, index) => (
                                                    <div key={index} className="list-group-item">
                                                        <div className="d-flex justify-content-between align-items-center">
                                                            <div>
                                                                <p className="mb-0 font-monospace small">**** **** **** {card.pan?.slice(-4)}</p>
                                                                <small className="text-muted">{card.card_type}</small>
                                                            </div>
                                                            <span className={`badge ${card.status === 'Active' ? 'bg-success' : 'bg-secondary'}`}>
                                                                {card.status}
                                                            </span>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <div className="text-center text-muted py-5">
                                    <i className="bi bi-credit-card" style={{ fontSize: '3rem' }}></i>
                                    <p className="mt-3">No hay cuenta cargada</p>
                                    <small>Cree una nueva cuenta o busque una existente</small>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
