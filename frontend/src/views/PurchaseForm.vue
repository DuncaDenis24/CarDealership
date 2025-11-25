<template>
  <div class="purchase-form">
    <!-- Success Popup -->
    <div v-if="showSuccessPopup" class="popup-overlay" @click.self="closePopup">
      <div class="popup">
        <div class="popup-content">
          <h3>Thank You!</h3>
          <p>Your purchase is pending. Our team will contact you shortly to confirm the details.</p>
          <button @click="closePopup" class="btn btn-primary">OK</button>
        </div>
      </div>
    </div>
    <div v-if="loading" class="loading">Loading car details...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <template v-else>
      <h2>Purchase {{ car.name }} {{ car.model }}</h2>
      
      <div class="car-summary">
        <div class="car-image-container">
          <img 
            :src="getCarImageUrl(car)" 
            :alt="`${car.make || ''} ${car.model || ''}`" 
            class="car-image"
            @error="handleImageError"
            loading="lazy"
          >
        </div>
        <div class="car-details-grid">
          <h3>{{ car.make || '' }} {{ car.model || '' }}</h3>
          
          <div class="car-specs">
            <div class="spec-group">
              <h4>Basic Information</h4>
              <div class="spec-row" v-if="car.type">
                <span class="spec-label">Type:</span>
                <span class="spec-value">{{ car.type }}</span>
              </div>
              <div class="spec-row" v-if="car.year">
                <span class="spec-label">Year:</span>
                <span class="spec-value">{{ car.year }}</span>
              </div>
              <div class="spec-row" v-if="car.color">
                <span class="spec-label">Color:</span>
                <span class="spec-value">
                  <span class="color-dot" :style="{ backgroundColor: car.color.toLowerCase() }"></span>
                  {{ car.color }}
                </span>
              </div>
              <div class="spec-row" v-if="car.transmission">
                <span class="spec-label">Transmission:</span>
                <span class="spec-value">{{ car.transmission }}</span>
              </div>
              <div class="spec-row" v-if="car.licensePlate">
                <span class="spec-label">License Plate:</span>
                <span class="spec-value">{{ car.licensePlate }}</span>
              </div>
            </div>

            <div class="spec-group">
              <h4>Pricing</h4>
              <div class="spec-row" v-if="car.price">
                <span class="spec-label">Price:</span>
                <span class="spec-value">${{ car.price.toLocaleString() }}</span>
              </div>
            </div>

            <div class="spec-group" v-if="car.mileage || car.fuelType || car.seats">
              <h4>Additional Info</h4>
              <div class="spec-row" v-if="car.mileage">
                <span class="spec-label">Mileage:</span>
                <span class="spec-value">{{ car.mileage.toLocaleString() }} km</span>
              </div>
              <div class="spec-row" v-if="car.fuelType">
                <span class="spec-label">Fuel Type:</span>
                <span class="spec-value">{{ car.fuelType }}</span>
              </div>
              <div class="spec-row" v-if="car.seats">
                <span class="spec-label">Seats:</span>
                <span class="spec-value">{{ car.seats }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <form @submit.prevent="submitPurchase" class="purchase-form-fields">
        <div class="form-group">
          <label for="customerName">Full Name</label>
          <input 
            type="text" 
            id="customerName" 
            v-model="purchaseData.customerName" 
            required
          >
        </div>
        
        <div class="form-group">
          <label for="customerEmail">Email</label>
          <input 
            type="email" 
            id="customerEmail" 
            v-model="purchaseData.customerEmail" 
            required
          >
        </div>
        
        <div class="form-group">
          <label for="customerPhone">Phone Number</label>
          <input 
            type="tel" 
            id="customerPhone" 
            v-model="purchaseData.customerPhone" 
            required
            placeholder="+40 7XX XXX XXX"
            pattern="[0-9+\s-]+"
          >
        </div>
        
        <div class="form-group">
          <label for="customerAddress">Shipping Address</label>
          <textarea 
            id="customerAddress" 
            v-model="purchaseData.customerAddress" 
            rows="3"
            required
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="paymentMethod">Payment Method</label>
          <select 
            id="paymentMethod" 
            v-model="purchaseData.paymentMethod"
            required
          >
            <option value="CASH">Cash</option>
            <option value="CREDIT_CARD">Credit Card</option>
            <option value="BANK_TRANSFER">Bank Transfer</option>
            <option value="LEASING">Leasing</option>
          </select>
        </div>
        
        <div class="form-actions">
          <div class="price-summary">
            <p>Total Amount: <strong>${{ car.price.toLocaleString() }}</strong></p>
          </div>
          <div class="buttons">
            <button 
              type="button" 
              @click="$router.go(-1)" 
              class="btn-cancel"
              :disabled="submitting"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              class="btn-submit"
              :disabled="submitting"
            >
              {{ submitting ? 'Processing...' : 'Complete Purchase' }}
            </button>
          </div>
        </div>
      </form>
    </template>
  </div>
</template>

<script>
import carService from '@/services/carService';
import purchaseService from '@/services/purchaseService';

export default {
  name: 'PurchaseForm',
  props: {
    carId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      car: null,
      loading: true,
      error: null,
      showSuccessPopup: false,
      submitting: false,
      purchaseData: {
        customerName: '',
        customerEmail: '',
        customerPhone: '',
        customerAddress: '',
        paymentMethod: 'CREDIT_CARD',
        purchasePrice: 0
      }
    };
  },
  async created() {
    await this.fetchCar();
  },
  methods: {
    getCarImageUrl(car) {
      if (!car) return this.getFallbackImage();
      
      if (car.imageUrl) {
        if (car.imageUrl.includes('Masini/')) {
          const filename = car.imageUrl.split('Masini/').pop();
          return `/Masini/${filename}`;
        }
        if (!car.imageUrl.startsWith('http') && !car.imageUrl.startsWith('/')) {
          return `/Masini/${car.imageUrl}`;
        }
        return car.imageUrl;
      }
      
      return this.getFallbackImage(car.type);
    },
    
    getFallbackImage(type) {
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
      if (event.target.src && event.target.src.startsWith('data:image/svg+xml')) {
        return;
      }
      event.target.src = this.getFallbackImage();
      event.target.style.display = 'block';
    },
    async fetchCar() {
      this.loading = true;
      this.error = null;
      
      try {
        this.car = await carService.getCarById(this.carId);
        this.purchaseData.purchasePrice = this.car.price;
      } catch (err) {
        console.error('Error fetching car:', err);
        this.error = 'Failed to load car details. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    
    
    closePopup() {
      this.showSuccessPopup = false;
      this.$router.push('/');
    },

    async submitPurchase() {
      this.submitting = true;
      
      try {
        const purchaseData = {
          carId: this.car.id,
          customerName: this.purchaseData.customerName,
          customerEmail: this.purchaseData.customerEmail,
          customerPhone: this.purchaseData.customerPhone,
          customerAddress: this.purchaseData.customerAddress,
          paymentMethod: this.purchaseData.paymentMethod,
          purchasePrice: this.car.price,
          status: 'PENDING' // Add status to indicate the purchase is pending
        };
        
        await purchaseService.createPurchase(purchaseData);
        this.showSuccessPopup = true;
      } catch (err) {
        console.error('Error creating purchase:', err);
        this.message('Failed to complete purchase. Please try again.');
      } finally {
        this.submitting = false;
      }
    }
  }
};
</script>

<style scoped>
/* Car Summary Section */
.car-summary {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.car-image-container {
  flex: 0 0 40%;
  max-width: 400px;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.car-image {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
}

.car-details-grid {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.car-details-grid h3 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  color: #2c3e50;
}

.car-specs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 0.5rem;
}

.spec-group {
  background: #f8f9fa;
  padding: 1.25rem;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.spec-group h4 {
  margin: 0 0 1rem;
  font-size: 1rem;
  color: #495057;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 0.5rem;
}

.spec-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f3f5;
}

.spec-row:last-child {
  border-bottom: none;
}

.spec-label {
  color: #6c757d;
  font-weight: 500;
}

.spec-value {
  color: #212529;
  font-weight: 500;
  text-align: right;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.color-dot {
  display: inline-block;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 1px solid #dee2e6;
  vertical-align: middle;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .car-summary {
    flex-direction: column;
  }
  
  .car-image-container {
    max-width: 100%;
  }
}

@media (max-width: 576px) {
  .car-specs {
    grid-template-columns: 1fr;
  }
}

/* Form styles */
.purchase-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.car-summary {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  align-items: center;
}

.car-image {
  width: 300px;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.car-info {
  flex: 1;
}

.car-info h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
}

.car-info p {
  margin: 0.5rem 0;
  color: #555;
}

.purchase-form-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="tel"],
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
  font-family: inherit;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.form-actions {
  grid-column: 1 / -1;
  margin-top: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.price-summary {
  font-size: 1.2rem;
  font-weight: 500;
  color: #28a745;
}

.buttons {
  display: flex;
  gap: 1rem;
}

.btn-submit,
.btn-cancel {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-submit {
  background-color: #28a745;
  color: white;
  border: 1px solid #28a745;
}

.btn-submit:hover:not(:disabled) {
  background-color: #218838;
  border-color: #1e7e34;
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: #f8f9fa;
  color: #6c757d;
  border: 1px solid #ddd;
}

.btn-cancel:hover:not(:disabled) {
  background-color: #e2e6ea;
  border-color: #dae0e5;
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
}

/* Popup styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 90%;
  width: 400px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.popup h3 {
  margin-top: 0;
  color: #2c3e50;
}

.popup p {
  margin: 1rem 0;
  font-size: 1.1rem;
  color: #333;
}

.popup .btn {
  margin-top: 1rem;
  padding: 0.5rem 2rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.popup .btn:hover {
  background-color: #218838;
}

@media (max-width: 768px) {
  .car-summary {
    flex-direction: column;
    text-align: center;
  }
  
  .car-image {
    width: 100%;
    height: auto;
    max-height: 200px;
  }
  
  .purchase-form-fields {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .buttons {
    width: 100%;
  }
  
  .btn-submit,
  .btn-cancel {
    flex: 1;
  }
}
</style>
