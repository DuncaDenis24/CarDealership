import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
    baseURL: '/api/cars', // Use full URL for development
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
    withCredentials: false // Disable credentials for now to avoid CORS issues
});

export default {
    async getAllAvailableCars() {
        // Get all available cars (including those only for sale)
        const response = await api.get('/all-available');
        return response.data;
    },
    
    async getFilteredCars(filter = 'all') {
        // First get all available cars
        const cars = await this.getAllAvailableCars();
        
        // Then filter based on the selected filter
        switch(filter) {
            case 'rent':
                return cars.filter(car => car.forRent);
            case 'sale':
                return cars.filter(car => car.forSale);
            case 'all':
            default:
                return cars;
        }
    },
    
    async getCarById(id) {
        const response = await api.get(`/${id}`);
        return response.data;
    },
    
    // Get all cars (alias for getAllAvailableCars for backward compatibility)
    async getAvailableCars() {
        return this.getAllAvailableCars();
    },
    
    // Get cars marked for sale
    async getCarsForSale() {
        const cars = await this.getAllAvailableCars();
        return cars.filter(car => car.forSale === true);
    },
    
    // Get cars marked for rent
    async getAvailableForRent() {
        const cars = await this.getAllAvailableCars();
        return cars.filter(car => car.forRent === true);
    },
    
    async createCar(carData) {
        const response = await api.post('', carData);
        return response.data;
    },
    
    async updateCar(id, carData) {
        const response = await api.put(`/${id}`, carData);
        return response.data;
    },
    
    async deleteCar(id) {
        await api.delete(`/${id}`);
    },
    
    async calculateRentalPrice(carId, startDate, endDate) {
        try {
            const response = await fetch(`/api/rentals/calculate-price?carId=${carId}&startDate=${startDate}&endDate=${endDate}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                credentials: 'include'  // Important for sending cookies if using sessions
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Failed to calculate price');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error calculating price:', error);
            throw error;
        }
    }
};
