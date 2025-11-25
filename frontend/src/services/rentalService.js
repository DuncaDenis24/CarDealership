import axios from 'axios';

const API_URL = '/api/rentals';

export default {
    async getAllRentals() {
        const response = await axios.get(API_URL);
        return response.data;
    },
    
    async getRentalById(id) {
        const response = await axios.get(`${API_URL}/${id}`);
        return response.data;
    },
    
    async createRental(rentalData) {
        const response = await axios.post(API_URL, rentalData);
        return response.data;
    },
    
    async updateRental(id, rentalData) {
        const response = await axios.put(`${API_URL}/${id}`, rentalData);
        return response.data;
    },
    
    async deleteRental(id) {
        await axios.delete(`${API_URL}/${id}`);
    },
    
    async getRentalsByEmail(email) {
        const response = await axios.get(`${API_URL}/email/${email}`);
        return response.data;
    },
    
    async getActiveRentals() {
        const response = await axios.get(`${API_URL}/active`);
        return response.data;
    },
    
    async getRentalsInDateRange(startDate, endDate) {
        const response = await axios.get(`${API_URL}/date-range`, {
            params: { startDate, endDate }
        });
        return response.data;
    },

    async getRentalsInDateRangeForCar(carId, startDate, endDate) {
        const response = await axios.get(`${API_URL}/date-range/car/${carId}`, {
            params: { 
                start: startDate,
                end: endDate 
            }
        });
        return response.data;
    },
    
    async cancelRental(id) {
        const response = await axios.put(`${API_URL}/${id}/status`, { status: 'CANCELLED' });
        return response.data;
    }
};
