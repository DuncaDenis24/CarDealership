<template>
  <div class="car-list">
    <!-- AI Chat Component -->
    <AIChat 
      :cars="allCars" 
      @apply-filters="applyAIFilters"
      @update:cars="handleUpdatedCars"
    />
    <h1>Available Cars</h1>
    
    <!-- Quick Filter Tabs -->
    <div class="quick-filters">
      <button 
        @click="setFilter('all')" 
        :class="['filter-tab', { 'active': activeFilter === 'all' }]"
      >
        All Cars
      </button>
      <button 
        @click="setFilter('rent')" 
        :class="['filter-tab', { 'active': activeFilter === 'rent' }]"
      >
        For Rent
      </button>
      <button
        @click="setFilter('sale')" 
        :class="['filter-tab', { 'active': activeFilter === 'sale' }]"
      >
        For Sale
      </button>
    </div>
    
    <div class="filters">
      <div class="filter-group">
        <label>Car Type:</label>
        <select v-model="filters.type">
          <option value="">All Types</option>
          <option v-for="type in carTypes" :key="type" :value="type">{{ type }}</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Min Price:</label>
        <input 
          type="number" 
          v-model.number="filters.minPrice" 
          :placeholder="activeFilter === 'rent' ? 'Min daily rate' : 'Min price'"
        >
      </div>
      <div class="filter-group">
        <label>Max Price:</label>
        <input 
          type="number" 
          v-model.number="filters.maxPrice" 
          :placeholder="activeFilter === 'rent' ? 'Max daily rate' : 'Max price'"
        >
      </div>
      <button @click="resetFilters" class="reset-btn">Reset Filters</button>
    </div>

    <div v-if="loading" class="loading">Loading cars...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="filteredCars.length === 0" class="no-results">No cars found matching your criteria.</div>

    <div v-else class="car-grid">
      <div v-for="car in filteredCars" :key="car.id" class="car-card">
        <div class="car-image">
          <img
            :src="getCarImageUrl(car)"
            :alt="`${car.name || ''} ${car.model || ''}`"
            @error="handleImageError"
            class="car-image"
            loading="lazy"
          >
        </div>
        <div class="car-details">
          <h3>{{ car.name }} {{ car.model }}</h3>
          <p class="car-type">{{ car.type }}</p>
          <p class="car-year">Year: {{ car.year }}</p>
          <p class="car-price" v-if="car.forSale">Price: ${{ car.price.toLocaleString() }}</p>
          <p class="car-daily-rate" v-else>Daily Rate: ${{ car.dailyRate.toLocaleString() }}</p>

          <div class="car-actions">
            <template v-if="activeFilter === 'all'">
              <template v-if="car.forRent && car.forSale">
                <router-link
                  :to="`/rent-car/${car.id}`"
                  class="btn-rent"
                >
                  Rent Now
                </router-link>
                <router-link
                  :to="`/buy-car/${car.id}`"
                  class="btn-buy"
                >
                  Buy Now
                </router-link>
              </template>
              <template v-else>
                <router-link
                  v-if="car.forRent"
                  :to="`/rent-car/${car.id}`"
                  class="btn-rent"
                >
                  Rent Now
                </router-link>
                <router-link
                  v-if="car.forSale"
                  :to="`/buy-car/${car.id}`"
                  class="btn-buy"
                >
                  Buy Now
                </router-link>
              </template>
            </template>
            <template v-else-if="activeFilter === 'rent'">
              <router-link
                :to="`/rent-car/${car.id}`"
                class="btn-rent"
              >
                Rent Now
              </router-link>
            </template>
            <template v-else-if="activeFilter === 'sale'">
              <router-link
                :to="`/buy-car/${car.id}`"
                class="btn-buy"
              >
                Buy Now
              </router-link>
            </template>
            <!-- Removed Details button as details are shown in rent/sale forms -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import carService from '@/services/carService';
import AIChat from '../components/AIChat.vue';

export default {
  name: 'CarList',
  components: {
    AIChat
  },
  data() {
    return {
      cars: [],
      allCars: [],
      loading: false,
      error: null,
      activeFilter: 'all',
      carTypes: ['SEDAN', 'SUV', 'HATCHBACK', 'CONVERTIBLE', 'SPORTS', 'MINIVAN', 'PICKUP'],
      filters: {
        type: '',
        minPrice: null,
        maxPrice: null,
        minYear: null,
        maxYear: null,
        transmission: ''
      },
      aiActiveFilters: {}
    };
  },
  data() {
    return {
      cars: [],
      allCars: [],
      loading: false,
      error: null,
      activeFilter: 'all',
      carTypes: ['SEDAN', 'SUV', 'HATCHBACK', 'CONVERTIBLE', 'SPORTS', 'MINIVAN', 'PICKUP'],
      filters: {
        type: '',
        minPrice: null,
        maxPrice: null,
        minYear: null,
        maxYear: null,
        transmission: ''
      },
      aiFilters: null, // Store AI filters separately
      aiFilteredCars: null // Store AI filtered cars directly
    };
  },
  computed: {
    filteredCars() {
      // If we have AI filtered cars, use them directly
      if (this.aiFilteredCars) {
        console.log('Using AI filtered cars:', this.aiFilteredCars);
        return this.aiFilteredCars;
      }
      
      // Otherwise, apply regular filters
      console.log('Filtering cars with regular filters:', this.filters);
      
      return this.cars.filter(car => {
        if (!car) return false;
        
        // Type filter
        if (this.filters.type && car.type && 
            !car.type.toLowerCase().includes(this.filters.type.toLowerCase())) {
          return false;
        }
        
        // Price filter (handle both price and dailyRate)
        const price = car.price || car.dailyRate || 0;
        if (this.filters.minPrice && price < this.filters.minPrice) return false;
        if (this.filters.maxPrice && price > this.filters.maxPrice) return false;
        
        // Year filter
        if (this.filters.minYear && car.year < this.filters.minYear) return false;
        if (this.filters.maxYear && car.year > this.filters.maxYear) return false;
        
        // Transmission filter
        if (this.filters.transmission && car.transmission && 
            !car.transmission.toLowerCase().includes(this.filters.transmission.toLowerCase())) {
          return false;
        }
        
        return true;
      });
    }
  },
  async created() {
    await this.fetchCars();
  },
  methods: {
    // Handle updated cars from AI
    handleUpdatedCars(updatedCars) {
      console.log('Received updated cars from AI:', updatedCars);
      
      if (updatedCars && Array.isArray(updatedCars)) {
        console.log('Setting AI filtered cars:', updatedCars.length, 'cars');
        
        // Store the AI filtered cars directly
        this.aiFilteredCars = [...updatedCars];
        
        // Show a toast notification
        if (this.$toast) {
          this.$toast.success(`Found ${updatedCars.length} matching cars`, {
            position: 'top-right',
            duration: 2000
          });
        }
      } else {
        console.error('Invalid cars data received from AI:', updatedCars);
        this.aiFilteredCars = null;
      }
      
      // Force Vue to re-render the component
      this.$nextTick(() => {
        this.$forceUpdate();
      });
    },
    
    // Update available car types from current car list
    updateCarTypes() {
      try {
        const types = new Set();
        this.cars.forEach(car => {
          if (car && car.type) {
            types.add(car.type.toUpperCase());
          }
        });
        this.carTypes = Array.from(types).sort();
      } catch (error) {
        console.error('Error updating car types:', error);
        this.carTypes = [];
      }
    },

    // Apply filters from AI chat
    applyAIFilters(filters) {
      console.log('Applying AI filters:', filters);
      
      // Store AI filters
      this.aiFilters = { ...filters };
      
      // If no filters, clear AI filtered cars
      if (!filters || Object.keys(filters).length === 0) {
        this.aiFilteredCars = null;
        return;
      }
      
      // Apply filters to the current car list
      this.aiFilteredCars = this.cars.filter(car => {
        if (!car) return false;
        
        // Type filter
        if (filters.type && car.type && 
            !car.type.toLowerCase().includes(filters.type.toLowerCase())) {
          return false;
        }
        
        // Price filter (handle both price and dailyRate)
        const price = car.price || car.dailyRate || 0;
        if (filters.minPrice && price < filters.minPrice) return false;
        if (filters.maxPrice && price > filters.maxPrice) return false;
        
        // Year filter
        if (filters.minYear && car.year < filters.minYear) return false;
        if (filters.maxYear && car.year > filters.maxYear) return false;
        
        // Transmission filter
        if (filters.transmission && car.transmission && 
            !car.transmission.toLowerCase().includes(filters.transmission.toLowerCase())) {
          return false;
        }
        
        return true;
      });
      
      console.log('AI filtered cars:', this.aiFilteredCars);
      
      // Update the active filter tab
      if (filters.type) {
        this.activeFilter = 'all';
      }
      
      // Force update to show the filtered cars
      this.$nextTick(() => {
        this.$forceUpdate();
      });
    },
    async fetchCars() {
      this.loading = true;
      this.error = null;
      try {
        // Get all available cars from the backend
        const response = await carService.getAvailableCars();
        
        if (!Array.isArray(response)) {
          throw new Error('Invalid response format from server');
        }
        
        // Process the cars to ensure they have all required properties
        this.allCars = response.map(car => {
          if (!car) return null;
          return {
            ...car,
            // Ensure required properties have default values
            id: car.id || Math.random().toString(36).substr(2, 9),
            imageUrl: car.imageUrl || this.getFallbackImage(car.type),
            price: Number(car.price) || 0,
            dailyRate: Number(car.dailyRate) || 0,
            year: Number(car.year) || new Date().getFullYear(),
            forSale: car.forSale !== undefined ? Boolean(car.forSale) : false,
            forRent: car.forRent !== undefined ? Boolean(car.forRent) : true,
            transmission: (car.transmission || 'Automatic').toString()
          };
        }).filter(Boolean); // Remove any null entries
        
        // Update the cars array to trigger reactivity
        this.cars = [...this.allCars];
        
        // Update available car types
        this.updateCarTypes();
        
      } catch (error) {
        console.error('Error fetching cars:', error);
        const errorMessage = error.response?.data?.message || 'Failed to load cars. Please try again later.';
        this.error = errorMessage;
        if (this.$toast) {
          this.$toast.error(errorMessage, { position: 'top-right' });
        }
      } finally {
        this.loading = false;
      }
    },
    getCarImageUrl(car) {
      if (!car) return this.getFallbackImage();
      
      // If imageUrl is provided and not empty, use it
      if (car.imageUrl) {
        // If it's a full local path, extract just the filename
        if (car.imageUrl.includes('Masini/')) {
          const filename = car.imageUrl.split('Masini/').pop();
          return `/Masini/${filename}`;
        }
        // If it's just a filename, add the Masini path
        if (!car.imageUrl.startsWith('http') && !car.imageUrl.startsWith('/')) {
          return `/Masini/${car.imageUrl}`;
        }
        return car.imageUrl;
      }
      
      // Fallback to type-based image
      return this.getFallbackImage(car.type);
    },
    
    getFallbackImage(type) {
      // Create a simple SVG placeholder
      const createPlaceholder = (text) => {
        const svg = `
          <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#f0f0f0"/>
            <text x="50%" y="50%" 
                  font-family="Arial, sans-serif" 
                  font-size="16" 
                  text-anchor="middle" 
                  dominant-baseline="middle"
                  fill="#666">
              ${text}
            </text>
          </svg>
        `;
        return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
      };

      const carType = (type || '').toUpperCase();
      const placeholders = {
        'SEDAN': createPlaceholder('Sedan'),
        'SUV': createPlaceholder('SUV'),
        'HATCHBACK': createPlaceholder('Hatchback'),
        'CONVERTIBLE': createPlaceholder('Convertible'),
        'SPORTS': createPlaceholder('Sports'),
        'MINIVAN': createPlaceholder('Minivan'),
        'PICKUP': createPlaceholder('Pickup')
      };
      
      return placeholders[carType] || createPlaceholder('Car');
    },
    
    handleImageError(event) {
      // Prevent infinite loop if the fallback also fails
      if (event.target.src && event.target.src.startsWith('data:image/svg+xml')) {
        return;
      }
      console.warn('Image failed to load, using fallback');
      event.target.src = this.getFallbackImage();
      event.target.style.display = 'block';
    },
    
    resetFilters() {
      // Store the current active filter
      const currentFilter = this.activeFilter;
      
      // Reset all filters except the active tab
      this.filters = {
        type: '',
        minPrice: null,
        maxPrice: null,
        minYear: null,
        maxYear: null,
        transmission: ''
      };
      
      // Clear AI filters and filtered cars
      this.aiFilters = null;
      this.aiFilteredCars = null;
      
      // Reload the current filter
      if (currentFilter === 'all') {
        this.cars = [...this.allCars];
      } else if (currentFilter === 'rent') {
        this.cars = this.allCars.filter(car => car.forRent);
      } else if (currentFilter === 'sale') {
        this.cars = this.allCars.filter(car => car.forSale);
      }
      
      // Update available car types
      this.updateCarTypes();
      
      // Force update to refresh the view
      this.$nextTick(() => {
        this.$forceUpdate();
      });
    },

    async setFilter(filterType) {
      this.activeFilter = filterType;
      this.loading = true;
      this.error = null;
      
      try {
        // Clear any AI filters when changing the main filter
        this.aiFilteredCars = null;
        this.aiFilters = null;
        
        if (filterType === 'all') {
          this.cars = await carService.getAvailableCars();
          this.allCars = [...this.cars]; // Update allCars with the full list
        } else if (filterType === 'rent') {
          const rentedCars = await carService.getAvailableForRent();
          this.cars = rentedCars;
          this.allCars = [...rentedCars]; // Update allCars with rented cars
        } else if (filterType === 'sale') {
          const saleCars = await carService.getCarsForSale();
          this.cars = saleCars;
          this.allCars = [...saleCars]; // Update allCars with cars for sale
        }

        // Reset other filters when changing the main filter
        this.resetFilters();
      } catch (err) {
        console.error('Error filtering cars:', err);
        this.error = 'Failed to filter cars. Please try again.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
:root {
  --primary: #4361ee;
  --primary-dark: #3a56d4;
  --accent: #4cc9f0;
  --success: #4caf50;
  --warning: #f8961e;
  --danger: #f94144;
  --light: #f8f9fa;
  --dark: #212529;
  --gray: #6c757d;
  --light-gray: #e9ecef;
  --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --card-hover-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Base styles */
.car-list {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  background-color: #f5f7fa;
  min-height: calc(100vh - 64px);
}

h1 {
  text-align: center;
  margin-bottom: 2.5rem;
  color: var(--dark);
  font-size: 2.5rem;
  font-weight: 700;
  position: relative;
  padding-bottom: 0.5rem;
}

h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
  border-radius: 2px;
}

/* Quick filter tabs */
.quick-filters {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin: 0 auto 2.5rem;
  flex-wrap: wrap;
  max-width: 800px;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.filter-tab {
  padding: 0.9rem 2.2rem;
  border: 2px solid #e2e8f0;
  border-radius: 50px;
  background: #ffffff;
  color: #4a5568;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: 0.5px;
  text-transform: uppercase;
  position: relative;
  overflow: hidden;
  z-index: 1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-tab::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  z-index: -1;
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: scale(0.95);
  border-radius: 50px;
}

.filter-tab:hover {
  color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(67, 97, 238, 0.25);
  border-color: var(--primary);
  background: linear-gradient(135deg, var(--primary), var(--accent));
}

.filter-tab:hover::before {
  opacity: 1;
  transform: scale(1);
}

.filter-tab.active {
  background: linear-gradient(135deg, var(--primary), #2a4bd8);
  color: white !important;
  box-shadow: 0 6px 15px rgba(67, 97, 238, 0.3);
  border-color: var(--primary);
  font-weight: 700;
  transform: translateY(-1px);
}

.filter-tab.active:hover {
  background: linear-gradient(135deg, var(--primary), #1e3ec7);
  transform: translateY(-2px);
}

.filter-tab.active::before {
  opacity: 0;
  transform: scale(1);
}

/* Add focus styles for better accessibility */
.filter-tab:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.3);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .quick-filters {
    padding: 0.5rem;
    gap: 0.5rem;
  }
  
  .filter-tab {
    padding: 0.7rem 1.2rem;
    font-size: 0.85rem;
  }
}

/* Filters */
.filters {
  background: white;
  padding: 1.8rem;
  border-radius: 16px;
  margin-bottom: 3rem;
  box-shadow: var(--card-shadow);
  transition: var(--transition);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.filters:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-bottom: 1.2rem;
}

.filter-group {
  flex: 1;
  min-width: 220px;
}

.filter-group label {
  display: block;
  margin-bottom: 0.6rem;
  font-weight: 600;
  color: var(--dark);
  font-size: 0.95rem;
}

.filter-group select,
.filter-group input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  transition: var(--transition);
  background-color: #f8fafc;
  color: var(--dark);
}

.filter-group select:focus,
.filter-group input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
  background-color: white;
}

.reset-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 0.5rem auto 0;
  padding: 0.8rem 2rem;
  background: white;
  color: var(--danger);
  border: 1px solid var(--danger);
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  transition: var(--transition);
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.reset-btn:hover {
  background: var(--danger);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(249, 65, 68, 0.2);
}

/* Loading, Error, No Results */
.loading,
.error,
.no-results {
  text-align: center;
  padding: 3rem 1rem;
  font-size: 1.2rem;
  color: var(--gray);
  background: white;
  border-radius: 12px;
  box-shadow: var(--card-shadow);
  margin: 2rem 0;
}

.error {
  color: var(--danger);
  background-color: #fef2f2;
  border-left: 4px solid var(--danger);
}

/* Car grid */
.car-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  margin-top: 1.5rem;
  padding: 0.5rem;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.car-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--card-shadow);
  transition: var(--transition);
  display: flex;
  flex-direction: column;
  position: relative;
  border: 1px solid rgba(0, 0, 0, 0.05);
  opacity: 0;
  animation: fadeIn 0.5s ease-out forwards;
}

.car-card:nth-child(1) { animation-delay: 0.1s; }
.car-card:nth-child(2) { animation-delay: 0.2s; }
.car-card:nth-child(3) { animation-delay: 0.3s; }
.car-card:nth-child(n+4) { animation-delay: 0.4s; }

.car-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--card-hover-shadow);
}

.car-image {
  height: 220px;
  overflow: hidden;
  position: relative;
}

.car-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.car-card:hover .car-image img {
  transform: scale(1.08);
}

.car-details {
  padding: 1.8rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  position: relative;
}

.car-details h3 {
  margin: 0 0 0.8rem;
  color: var(--dark);
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.3;
}

.car-type {
  display: inline-flex;
  align-items: center;
  background: rgba(67, 97, 238, 0.1);
  color: var(--primary);
  padding: 0.4rem 1rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  align-self: flex-start;
  transition: var(--transition);
}

.car-card:hover .car-type {
  background: var(--primary);
  color: white;
}

.car-specs {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin: 0.5rem 0 1.5rem;
}

.spec-item {
  display: flex;
  align-items: center;
  color: var(--gray);
  font-size: 0.9rem;
}

.spec-item i {
  margin-right: 0.5rem;
  color: var(--primary);
  font-size: 1.1rem;
}

.car-price-container {
  margin-top: auto;
  padding-top: 1.2rem;
  border-top: 1px dashed #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-label {
  font-size: 0.85rem;
  color: var(--gray);
  margin-bottom: 0.3rem;
}

.car-price,
.car-daily-rate {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--primary);
  line-height: 1.2;
}

.car-price span,
.car-daily-rate span {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--gray);
  margin-left: 0.3rem;
}

.car-actions {
  margin-top: 1.5rem;
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.btn-rent,
.btn-buy,
.btn-details {
  flex: 1;
  min-width: 100px;
  text-align: center;
  padding: 0.8rem 0.5rem;
  border-radius: 10px;
  font-weight: 600;
  text-decoration: none;
  transition: var(--transition);
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.btn-rent {
  background: var(--primary);
  color: white;
  box-shadow: 0 4px 15px rgba(67, 97, 238, 0.2);
}

.btn-buy {
  background: var(--success);
  color: white;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
}

.btn-rent:hover,
.btn-buy:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.btn-rent:active,
.btn-buy:active {
  transform: translateY(0);
}

/* Ripple effect */
.btn-rent::after,
.btn-buy::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, 0.5);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%, -50%);
  transform-origin: 50% 50%;
}

.btn-rent:hover::after,
.btn-buy:hover::after {
  animation: ripple 1s ease-out;
}

@keyframes ripple {
  0% {
    transform: scale(0, 0);
    opacity: 0.5;
  }
  100% {
    transform: scale(100, 100);
    opacity: 0;
  }
}

.availability-tag {
  position: absolute;
  top: 1.2rem;
  right: 1.2rem;
  background: rgba(255, 255, 255, 0.95);
  color: var(--success);
  padding: 0.4rem 1rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 700;
  z-index: 2;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.availability-tag::before {
  content: '';
  display: block;
  width: 8px;
  height: 8px;
  background: var(--success);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(76, 175, 80, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
  }
}

.car-badge {
  position: absolute;
  top: 1.2rem;
  left: 1.2rem;
  background: var(--accent);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 50px;
  font-size: 0.7rem;
  font-weight: 700;
  z-index: 2;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .car-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .car-list {
    padding: 1.5rem 1rem;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 2rem;
  }

  .filters {
    padding: 1.5rem;
  }

  .filter-row {
    flex-direction: column;
    gap: 1.2rem;
  }

  .filter-group {
    width: 100%;
  }

  .car-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1.5rem;
  }

  .car-details {
    padding: 1.5rem;
  }

  .car-actions {
    flex-direction: column;
  }

  .btn-rent,
  .btn-buy,
  .btn-details {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .car-grid {
    grid-template-columns: 1fr;
  }

  .filter-tab {
    padding: 0.6rem 1.2rem;
    font-size: 0.85rem;
  }

  .car-details h3 {
    font-size: 1.3rem;
  }

  .car-price,
  .car-daily-rate {
    font-size: 1.3rem;
  }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Print Styles */
@media print {
  .car-list {
    padding: 0;
    background: white;
  }

  .car-card {
    break-inside: avoid;
    box-shadow: none;
    border: 1px solid #eee;
    margin-bottom: 1rem;
  }

  .car-actions,
  .filter-tabs,
  .filter-options {
    display: none !important;
  }
}

.car-price {
  color: #27ae60;
  font-weight: 600;
  font-size: 1.1em;
}

.car-daily-rate {
  color: #e67e22;
  font-weight: 600;
  font-size: 1.1em;
}

.car-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.btn-rent, .btn-buy, .btn-details {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  text-decoration: none;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
}

.btn-rent {
  background: #3498db;
  color: white;
}

.btn-buy {
  background: #2ecc71;
  color: white;
}

.btn-details {
  background: #f1f1f1;
  color: #333;
}

.btn-rent:hover, .btn-buy:hover, .btn-details:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

/* Loading and error states */
.loading, .error, .no-results {
  text-align: center;
  padding: 40px;
  font-size: 1.2em;
  color: #666;
}

.error {
  color: #e74c3c;
}

/* Responsive design */
@media (max-width: 768px) {
  .filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .car-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
  
  .quick-filters {
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .car-actions {
    flex-direction: column;
  }
  
  .btn-rent, .btn-buy, .btn-details {
    width: 100%;
  }
}
.car-list {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.filters {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: flex-end;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

.filter-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.filter-group select,
.filter-group input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.reset-btn {
  padding: 0.5rem 1rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
  align-self: flex-end;
}

.reset-btn:hover {
  background-color: #5a6268;
}

.car-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 1.5rem;
}

.car-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.car-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.car-image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.car-details {
  padding: 1.25rem;
}

.car-details h3 {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  color: #333;
}

.car-type {
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0.25rem 0;
}

.car-year,
.car-price,
.car-daily-rate {
  margin: 0.5rem 0;
  color: #495057;
  font-weight: 500;
}

.car-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #eee;
}

.btn-rent,
.btn-buy,
.btn-details {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  text-align: center;
  flex: 1;
  transition: all 0.2s;
}

.btn-rent {
  background-color: #007bff;
  color: white;
  border: 1px solid #007bff;
}

.btn-rent:hover {
  background-color: #0069d9;
  border-color: #0062cc;
}

.btn-buy {
  background-color: #28a745;
  color: white;
  border: 1px solid #28a745;
}

.btn-buy:hover {
  background-color: #218838;
  border-color: #1e7e34;
}

.btn-details {
  background-color: #6c757d;
  color: white;
  border: 1px solid #6c757d;
}

.btn-details:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

.loading,
.error,
.no-results {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #6c757d;
}

.error {
  color: #dc3545;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .reset-btn {
    align-self: stretch;
  }
  
  .car-grid {
    grid-template-columns: 1fr;
  }
}
</style>
