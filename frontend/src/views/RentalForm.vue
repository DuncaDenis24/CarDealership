<template>
  <div class="rental-form">
      <!-- Error Modal -->
      <div v-if="showErrorModal" class="modal-overlay" @click.self="closeErrorModal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 9999; display: flex; justify-content: center; align-items: center;">
        <div style="background: white; padding: 30px; border-radius: 8px; max-width: 500px; width: 90%; position: relative; z-index: 10000; color: black;">
          <h3 style="margin-top: 0; color: #e74c3c;">⚠️ Date Conflict</h3>
          <p style="margin: 15px 0 20px;">{{ errorMessage || 'The selected dates are not available.' }}</p>
          <button @click="closeErrorModal" style="background: #e74c3c; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer;">
            I understand
          </button>
        </div>
      </div>
    <!-- Calendar Popup -->
    <div v-if="showCalendar" class="popup-overlay" @click.self="closeCalendar">
      <div class="popup calendar-popup">
        <div class="calendar">
          <div class="calendar-header">
            <button @click="prevMonth" class="nav-arrow">&lt;</button>
            <h3>{{ currentMonth }} {{ currentYear }}</h3>
            <button @click="nextMonth" class="nav-arrow">&gt;</button>
          </div>
          <div class="weekdays">
            <div v-for="day in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']" :key="day" class="weekday">{{ day }}</div>
          </div>
          <div class="days">
            <div 
              v-for="day in calendarDays" 
              :key="day.date"
              :class="[
                'day', 
                { 'other-month': !day.isCurrentMonth, 
                  'today': day.isToday, 
                  'selected': isSelected(day),
                  'disabled': !day.isAvailable || day.isPast
                }
              ]"
              @click="selectDate(day)"
            >
              {{ day.day }}
              <div v-if="!day.isAvailable" class="unavailable"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Success Popup -->
    <div v-if="showSuccessPopup" class="popup-overlay" @click.self="closePopup">
      <div class="popup">
        <div class="popup-content">
          <h3>Thank You!</h3>
          <p>Your order is pending. Our team will contact you shortly to confirm the details.</p>
          <button @click="closePopup" class="btn btn-primary">OK</button>
        </div>
      </div>
    </div>
    <div v-if="loading" class="loading">Loading car details...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else>
      <h2>Rent {{ car.name }} {{ car.model }}</h2>

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
            </div>

            <div class="spec-group">
              <h4>Pricing</h4>
              <div class="spec-row" v-if="car.dailyRate">
                <span class="spec-label">Daily Rate:</span>
                <span class="spec-value">${{ car.dailyRate.toFixed(2) }}</span>
              </div>
              <div v-if="priceInfo" class="spec-row total-price">
                <span class="spec-label">Total for {{ rentalDays }} day{{ rentalDays !== 1 ? 's' : '' }}:</span>
                <span class="spec-value">${{ priceInfo.totalPrice.toFixed(2) }}</span>
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

      <form @submit.prevent="submitRental" class="rental-form-fields">
        <div class="form-group">
          <label>Rental Period</label>
          <div class="date-range-picker">
            <div class="date-input" @click="openCalendar('start')">
              <label>Start Date</label>
              <div class="date-display">
                {{ rentalData.startDate || 'Select start date' }}
                <span class="calendar-icon">📅</span>
              </div>
            </div>
            <div class="date-separator">to</div>
            <div class="date-input" @click="openCalendar('end')">
              <label>End Date</label>
              <div class="date-display">
                {{ rentalData.endDate || 'Select end date' }}
                <span class="calendar-icon">📅</span>
              </div>
            </div>
          </div>
          <input type="hidden" v-model="rentalData.startDate" required>
          <input type="hidden" v-model="rentalData.endDate" required>
        </div>

        <div class="form-group">
          <label for="customerName">Your Name</label>
          <input
            type="text"
            id="customerName"
            v-model="rentalData.customerName"
            required
          >
        </div>

        <div class="form-group">
          <label for="customerEmail">Email</label>
          <input
            type="email"
            id="customerEmail"
            v-model="rentalData.customerEmail"
            required
          >
        </div>

        <div class="form-group">
          <label for="customerPhone">Phone Number</label>
          <input
            type="tel"
            id="customerPhone"
            v-model="rentalData.customerPhone"
            required
            placeholder="+40 7XX XXX XXX"
            @input="validatePhoneNumber"
          >
        </div>

        <div class="form-actions">
          <button type="submit" :disabled="submitting" class="btn-submit">
            {{ submitting ? 'Processing...' : 'Confirm Rental' }}
          </button>
          <button
            type="button"
            @click="$router.go(-1)"
            class="btn-cancel"
            :disabled="submitting"
          >
            Cancel
          </button>
        </div>
      </form>
    </template>
  </div>
</template>

<script>
import carService from '@/services/carService';
import rentalService from '@/services/rentalService';

export default {
  name: 'RentalForm',
  props: {
    carId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const currentDate = new Date();
    currentDate.setDate(1);

    return {
      car: null,
      loading: true,
      error: null,
      submitting: false,
      showErrorModal: false,
      errorMessage: '',
      today: today.toISOString().split('T')[0],
      rentalData: {
        startDate: '',
        endDate: '',
        customerName: '',
        customerEmail: ''
      },
      priceInfo: null,
      showCalendar: false,
      calendarMode: 'start', // 'start' or 'end'
      currentMonth: currentDate.toLocaleString('default', { month: 'long' }),
      currentYear: currentDate.getFullYear(),
      calendarDays: [],
      unavailableDates: [],
      selectedStartDate: null,
      selectedEndDate: null
    };
  },
  computed: {
    rentalDays() {
      if (!this.rentalData.startDate || !this.rentalData.endDate) return 0;
      const start = new Date(this.rentalData.startDate);
      const end = new Date(this.rentalData.endDate);
      return Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
    }
  },
  async created() {
    await this.fetchCar();
  },
  async created() {
    await this.fetchCar();
    await this.fetchUnavailableDates();
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
      } catch (err) {
        console.error('Error fetching car:', err);
        this.error = 'Failed to load car details. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    async calculatePrice() {
      if (!this.rentalData.startDate || !this.rentalData.endDate) {
        console.log('Start date or end date is missing');
        return;
      }

      console.log('Calculating price with:', {
        carId: this.car.id,
        startDate: this.rentalData.startDate,
        endDate: this.rentalData.endDate
      });

      try {
        const price = await carService.calculateRentalPrice(
          this.car.id,
          this.rentalData.startDate,
          this.rentalData.endDate
        );

        console.log('Received price from server:', price);

        this.priceInfo = {
          totalPrice: price,
          dailyRate: this.car.dailyRate,
          days: this.rentalDays
        };

        console.log('Updated priceInfo:', this.priceInfo);
      } catch (err) {
        console.error('Error calculating price:', {
          message: err.message,
          response: err.response ? {
            status: err.response.status,
            data: err.response.data
          } : 'No response data',
          stack: err.stack
        });
        this.$toast.error(`Failed to calculate rental price: ${err.message}`);
      }
    },


    showSuccessPopup: false,

    closePopup() {
      this.showSuccessPopup = false;
      this.$router.push('/');
    },
    
    openCalendar(mode) {
      this.calendarMode = mode;
      this.showCalendar = true;
      this.generateCalendar();
    },
    
    closeCalendar() {
      this.showCalendar = false;
    },
    
    prevMonth() {
      const date = new Date(this.currentYear, this.getMonthNumber(this.currentMonth) - 1, 1);
      date.setMonth(date.getMonth() - 1);
      this.currentMonth = date.toLocaleString('default', { month: 'long' });
      this.currentYear = date.getFullYear();
      this.generateCalendar();
    },
    
    nextMonth() {
      const date = new Date(this.currentYear, this.getMonthNumber(this.currentMonth) - 1, 1);
      date.setMonth(date.getMonth() + 1);
      this.currentMonth = date.toLocaleString('default', { month: 'long' });
      this.currentYear = date.getFullYear();
      this.generateCalendar();
    },
    
    getMonthNumber(monthName) {
      return new Date(`${monthName} 1, 2000`).getMonth() + 1;
    },
    
    async fetchUnavailableDates() {
      try {
        console.log('Fetching unavailable dates for car ID:', this.car.id);
        
        // Get rentals for the next 12 months
        const startDate = new Date();
        startDate.setHours(0, 0, 0, 0);
        
        const endDate = new Date();
        endDate.setMonth(endDate.getMonth() + 12);
        endDate.setHours(23, 59, 59, 999);
        
        console.log('Fetching rentals for car between:', startDate, 'and', endDate);
        
        // Use the new endpoint that filters by car ID
        const carRentals = await rentalService.getRentalsInDateRangeForCar(
          this.car.id,
          startDate.toISOString().split('T')[0],
          endDate.toISOString().split('T')[0]
        );
        
        console.log('Received rentals for car:', carRentals);
        
        // Get all dates in the rental periods
        this.unavailableDates = [];
        
        carRentals.forEach(rental => {
          const start = new Date(rental.startDate);
          const end = new Date(rental.endDate);
          
          console.log('Processing rental period:', start, 'to', end);
          
          // Add all dates in the rental period to unavailableDates
          const current = new Date(start);
          current.setHours(0, 0, 0, 0);
          
          const endDate = new Date(end);
          endDate.setHours(23, 59, 59, 999);
          
          while (current <= endDate) {
            const dateStr = current.toISOString().split('T')[0];
            if (!this.unavailableDates.includes(dateStr)) {
              this.unavailableDates.push(dateStr);
            }
            current.setDate(current.getDate() + 1);
          }
        });
        
        console.log('Unavailable dates:', this.unavailableDates);
        this.generateCalendar();
      } catch (error) {
        console.error('Error fetching unavailable dates:', error);
      }
    },
    
    generateCalendar() {
      const year = this.currentYear;
      const month = this.getMonthNumber(this.currentMonth) - 1; // 0-indexed
      
      // Get first day of month and total days in month
      const firstDay = new Date(year, month, 1).getDay();
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      const prevMonthDays = new Date(year, month, 0).getDate();
      
      // Adjust first day to be Monday (1) based
      const firstDayAdjusted = firstDay === 0 ? 6 : firstDay - 1;
      
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      const days = [];
      
      // Previous month days
      for (let i = firstDayAdjusted - 1; i >= 0; i--) {
        const day = prevMonthDays - i;
        const date = new Date(year, month - 1, day);
        days.push({
          day,
          date: date.toISOString().split('T')[0],
          isCurrentMonth: false,
          isToday: false,
          isAvailable: false,
          isPast: true
        });
      }
      
      // Current month days
      for (let i = 1; i <= daysInMonth; i++) {
        const date = new Date(year, month, i);
        const dateString = date.toISOString().split('T')[0];
        const isUnavailable = this.unavailableDates.includes(dateString);
        const isPast = date < today;

        days.push({
          day: i,
          date: dateString,
          isCurrentMonth: true,
          isToday: date.toDateString() === today.toDateString(),
          isAvailable: !isUnavailable && !isPast,
          isPast: isPast
        });
      }
      
      // Next month days to complete the grid (6 rows x 7 days = 42 cells)
      const remainingDays = 42 - days.length;
      for (let i = 1; i <= remainingDays; i++) {
        const date = new Date(year, month + 1, i);
        days.push({
          day: i,
          date: date.toISOString().split('T')[0],
          isCurrentMonth: false,
          isToday: false,
          isAvailable: false,
          isPast: date < today
        });
      }

      this.calendarDays = days;
    },

    selectDate(day) {
      if (!day.isAvailable || day.isPast) return;
      
      const selectedDate = day.date;
      
      if (this.calendarMode === 'start') {
        this.rentalData.startDate = selectedDate;
        this.rentalData.endDate = ''; // Reset end date when start date changes
        this.calendarMode = 'end';
      } else {
        // If end date is before start date, swap them
        if (new Date(selectedDate) < new Date(this.rentalData.startDate)) {
          this.rentalData.endDate = this.rentalData.startDate;
          this.rentalData.startDate = selectedDate;
        } else {
          this.rentalData.endDate = selectedDate;
        }
       // After setting both dates, check for conflicts
         const hasConflict = this.checkDateConflict(
            this.rentalData.startDate,
            this.rentalData.endDate
         );
         if (hasConflict) {
               this.showError('The selected period includes dates that are already booked or are not available. Please choose a different period.');
               this.rentalData.endDate = ''; // Clear the end date to force reselection
               this.generateCalendar();
               return;
             }
         this.showCalendar = false;
         this.calculatePrice();
      }
      
      this.generateCalendar();
    },
    
    isSelected(day) {
      if (!day.isCurrentMonth) return false;
      
      const date = day.date;
      const startDate = this.rentalData.startDate;
      const endDate = this.rentalData.endDate;
      
      if (!startDate) return false;
      if (!endDate) return date === startDate;
      
      const current = new Date(date);
      const start = new Date(startDate);
      const end = new Date(endDate);
      
      // Check if the date is within the selected range
      if (current >= start && current <= end) {
        // Check if this date is in an unavailable range
        const dateStr = current.toISOString().split('T')[0];
        if (this.unavailableDates.includes(dateStr)) {
          return false; // Don't mark as selected if it's an unavailable date
        }
        return true;
      }
      
      return false;
    },

    // Check if a date range conflicts with any existing rentals
    checkDateConflict(startDate, endDate) {
      if (!this.unavailableDates || this.unavailableDates.length === 0) return false;
      
      const start = new Date(startDate);
      const end = new Date(endDate);
      
      // Check each unavailable date
      for (const dateStr of this.unavailableDates) {
        const date = new Date(dateStr);
        if (date >= start && date <= end) {
          return true; // Conflict found
        }
      }
      return false; // No conflicts
    },
    
    // Validate phone number format
    validatePhoneNumber() {
      const phoneInput = this.$el?.querySelector('#customerPhone');
      if (!phoneInput) return;
      
      const value = phoneInput.value || '';
      const pattern = /^[0-9+\s-]*$/; // Allow empty input for better UX
      
      if (value && !pattern.test(value)) {
        phoneInput.setCustomValidity('Please enter a valid phone number (only digits, spaces, and + are allowed)');
      } else {
        phoneInput.setCustomValidity('');
      }
      
      // Force validation UI update
      phoneInput.reportValidity();
      
      // Return validation result for programmatic checks
      return !value || pattern.test(value);
    },
    
    // Format date to YYYY-MM-DD for comparison
    formatDate(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.toISOString().split('T')[0];
    },
    
    // Check if a date string is in YYYY-MM-DD format
    isValidDateString(dateStr) {
      return /^\d{4}-\d{2}-\d{2}$/.test(dateStr);
    },
    
    async submitRental() {
      try {
        // Basic validation
        if (!this.rentalData.startDate || !this.rentalData.endDate) {
          this.$toast.error('Please select both start and end dates');
          return;
        }

        // Validate phone number
        if (!this.validatePhoneNumber()) {
          this.$toast.error('Please enter a valid phone number');
          return;
        }

        // Format dates for comparison
        const startDate = this.formatDate(this.rentalData.startDate);
        const endDate = this.formatDate(this.rentalData.endDate);

        if (!this.isValidDateString(startDate) || !this.isValidDateString(endDate)) {
          this.$toast.error('Invalid date format. Please try again.');
          return;
        }

        // Check for date conflicts
        if (this.checkDateConflict(startDate, endDate)) {
          this.$toast.error('The selected period is not available. Please choose different dates.');
          return;
        }

        this.submitting = true;

        const rental = {
          car: { id: this.car?.id || this.$route.params.id },
          startDate: startDate,
          endDate: endDate,
          customerName: this.rentalData.customerName,
          customerEmail: this.rentalData.customerEmail,
          customerPhone: this.rentalData.customerPhone,
          totalPrice: this.priceInfo?.totalPrice || 0,
          status: 'PENDING'
        };

        console.log('Submitting rental:', rental);
        const response = await rentalService.createRental(rental);
        console.log('Rental created successfully:', response);
        this.showSuccessPopup = true;
      } catch (err) {
        console.error('Error creating rental:', {
          message: err.message,
          response: err.response?.data,
          status: err.response?.status,
          headers: err.response?.headers
        });
        
        // Handle different types of errors
        let errorMessage = 'Failed to create rental. Please try again.';
        
        if (err.response?.data) {
          // Handle server validation errors
          if (err.response.data.errors) {
            errorMessage = Object.values(err.response.data.errors)
              .flat()
              .join(' ');
          } else if (err.response.data.message) {
            errorMessage = err.response.data.message;
          }
        } else if (err.message) {
          errorMessage = err.message;
        }
        
        this.showError(errorMessage);
      } finally {
        this.submitting = false;
      }
    },
      showError(message) {
        console.log('Showing error modal with message:', message);
        this.errorMessage = message;
        this.showErrorModal = true;
      },

      closeErrorModal() {
        this.showErrorModal = false;
        this.errorMessage = '';
      }
  }
};
</script>

<style scoped>
.calendar-popup {
  max-width: 400px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.calendar {
  width: 100%;
  font-family: Arial, sans-serif;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.nav-arrow {
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
}

.nav-arrow:hover {
  background-color: #f0f0f0;
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  font-weight: bold;
  margin-bottom: 10px;
}

.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.day {
  padding: 8px;
  text-align: center;
  cursor: pointer;
  border-radius: 4px;
  position: relative;
}

.day:hover:not(.disabled) {
  background-color: #f0f8ff;
}

.day.today {
  font-weight: bold;
  color: #1a73e8;
}

.day.selected {
  background-color: #1a73e8;
  color: white;
}

.day.disabled {
  color: #ccc;
  cursor: not-allowed;
  position: relative;
}

.day.other-month {
  color: #aaa;
}

.day .unavailable {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 24px;
  height: 2px;
  background-color: #ff6b6b;
  opacity: 0.7;
}

.date-range-picker {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.date-input {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  transition: border-color 0.2s;
}

.date-input:hover {
  border-color: #aaa;
}

.date-input label {
  display: block;
  font-size: 0.9em;
  color: #666;
  margin-bottom: 4px;
}

.date-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.calendar-icon {
  font-size: 1.2em;
}

.date-separator {
  color: #666;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup {
  background: white;
  padding: 25px;
  border-radius: 8px;
  max-width: 90%;
  max-height: 90%;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.popup-content {
  text-align: center;
}

.popup h3 {
  margin-top: 0;
  color: #333;
}

.popup p {
  margin: 15px 0 20px;
  color: #555;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #1a73e8;
  color: white;
}

.btn-primary:hover {
  background-color: #1557b0;
}

.btn-cancel {
  background-color: #f1f3f4;
  color: #5f6368;
  margin-left: 10px;
}

.btn-cancel:hover {
  background-color: #e8eaed;
}
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

.total-price {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 2px solid #e9ecef;
}

.total-price .spec-value {
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
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
}

.popup button {
  margin-top: 1rem;
  padding: 0.5rem 2rem;
}

.rental-form {
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

.price-summary {
  margin-top: 1rem !important;
  font-size: 1.1rem;
  color: #28a745 !important;
  font-weight: 500;
}

.rental-form-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="date"] {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.form-actions {
  grid-column: 1 / -1;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.btn-submit,
.btn-cancel {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
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

  .rental-form-fields {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-submit,
  .btn-cancel {
    width: 100%;
  }
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.modal {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  animation: modalFadeIn 0.3s ease-out;
  position: relative;
  z-index: 10001;
  /* Debug styles */
  border: 2px solid #ff0000; /* Red border for visibility */
  transform: translateZ(0); /* Force hardware acceleration */
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f0f0;
}

.modal-header h3 {
  margin: 0;
  color: #e74c3c; /* Red color for error header */
  font-size: 1.4rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #7f8c8d;
  transition: color 0.2s;
}

.close-button:hover {
  color: #e74c3c;
}

.modal-body {
  margin-bottom: 25px;
  color: #333;
  font-size: 1.1rem;
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
}

.btn-ok {
  background-color: #e74c3c; /* Red color for error button */
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.btn-ok:hover {
  background-color: #c0392b; /* Darker red on hover */
}
</style>
