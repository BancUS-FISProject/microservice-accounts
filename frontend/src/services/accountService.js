import api from './api';

const accountService = {
    /**
     * POST /v1/accounts/
     * Crear una nueva cuenta
     * @param {Object} accountData - { name: string, email: string, subscription?: string }
     * @returns {Promise<Object>} AccountView
     */
    createAccount: async (accountData) => {
        try {
            const response = await api.post('/v1/accounts/', {
                name: accountData.name,
                email: accountData.email,
                subscription: accountData.subscription || 'Free'
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * GET /v1/accounts/{iban}
     * Obtener cuenta por IBAN
     * @param {string} iban - IBAN de la cuenta
     * @returns {Promise<Object>} AccountView
     */
    getAccountByIban: async (iban) => {
        try {
            const response = await api.get(`/v1/accounts/${iban}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * PATCH /v1/accounts/{iban}
     * Actualizar información de la cuenta (name, email, subscription)
     * @param {string} iban - IBAN de la cuenta
     * @param {Object} accountData - { name?: string, email?: string, subscription?: string }
     * @returns {Promise<Object>} AccountView
     */
    updateAccount: async (iban, accountData) => {
        try {
            const response = await api.patch(`/v1/accounts/${iban}`, accountData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * DELETE /v1/accounts/{iban}
     * Eliminar cuenta
     * @param {string} iban - IBAN de la cuenta
     * @returns {Promise<void>}
     */
    deleteAccount: async (iban) => {
        try {
            const response = await api.delete(`/v1/accounts/${iban}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * PATCH /v1/accounts/operation/{iban}
     * Actualizar balance de la cuenta (depositar o retirar)
     * @param {string} iban - IBAN de la cuenta
     * @param {number} balance - Cantidad a sumar (positivo) o restar (negativo)
     * @returns {Promise<Object>} AccountView
     */
    updateBalance: async (iban, balance) => {
        try {
            const response = await api.patch(`/v1/accounts/operation/${iban}`, {
                balance: balance
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * Helper: Depositar dinero (suma al balance)
     * @param {string} iban - IBAN de la cuenta
     * @param {number} amount - Cantidad a depositar (positivo)
     * @returns {Promise<Object>} AccountView
     */
    deposit: async (iban, amount) => {
        return accountService.updateBalance(iban, Math.abs(amount));
    },

    /**
     * Helper: Retirar dinero (resta del balance)
     * @param {string} iban - IBAN de la cuenta
     * @param {number} amount - Cantidad a retirar (positivo)
     * @returns {Promise<Object>} AccountView
     */
    withdraw: async (iban, amount) => {
        return accountService.updateBalance(iban, -Math.abs(amount));
    },

    /**
     * PATCH /v1/accounts/{iban}/block
     * Bloquear cuenta
     * @param {string} iban - IBAN de la cuenta
     * @returns {Promise<Object>} AccountView
     */
    blockAccount: async (iban) => {
        try {
            const response = await api.patch(`/v1/accounts/${iban}/block`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * PATCH /v1/accounts/{iban}/unblock
     * Desbloquear cuenta
     * @param {string} iban - IBAN de la cuenta
     * @returns {Promise<Object>} AccountView
     */
    unblockAccount: async (iban) => {
        try {
            const response = await api.patch(`/v1/accounts/${iban}/unblock`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * POST /v1/accounts/card/{iban}
     * Crear una nueva tarjeta asociada a la cuenta
     * @param {string} iban - IBAN de la cuenta
     * @returns {Promise<Object>} AccountView con la nueva tarjeta
     */
    createCard: async (iban) => {
        try {
            const response = await api.post(`/v1/accounts/card/${iban}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * DELETE /v1/accounts/card/{iban}
     * Eliminar una tarjeta de la cuenta
     * @param {string} iban - IBAN de la cuenta
     * @param {string} pan - Número de la tarjeta (PAN)
     * @returns {Promise<void>}
     */
    deleteCard: async (iban, pan) => {
        try {
            const response = await api.delete(`/v1/accounts/card/${iban}`, {
                data: { pan }
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * GET /v1/health
     * Verificar estado del servicio
     * @returns {Promise<Object>} { service: string, status: string }
     */
    healthCheck: async () => {
        try {
            const response = await api.get('/v1/health');
            return response.data;
        } catch (error) {
            throw error;
        }
    },
};

export default accountService;
