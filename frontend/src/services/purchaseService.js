import axios from 'axios';

const API_URL = '/api/purchases';

export default {
    async getAllPurchases() {
        const response = await axios.get(API_URL);
        return response.data;
    },
    
    async getPurchaseById(id) {
        const response = await axios.get(`${API_URL}/${id}`);
        return response.data;
    },
    
    async createPurchase(purchaseData) {
        const response = await axios.post(API_URL, purchaseData, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return response.data;
    },
    
    async deletePurchase(id) {
        await axios.delete(`${API_URL}/${id}`);
    },
    
    async getPurchasesByEmail(email) {
        const response = await axios.get(`${API_URL}/email/${email}`);
        return response.data;
    },
    
    async cancelPurchase(id) {
        const response = await axios.put(`${API_URL}/${id}/status`, { status: 'CANCELLED' });
        return response.data;
    }
};
