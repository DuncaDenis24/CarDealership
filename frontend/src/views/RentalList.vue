<template>
  <div class="list-container">
    <ConfirmationDialog
      :is-open="showConfirmDialog"
      title="Confirm Cancellation"
      :message="'Are you sure you want to cancel the rental for ' + (selectedRental ? selectedRental.car.name + ' ' + selectedRental.car.model : 'this car') + '?'"
      confirm-text="Yes, Cancel Rental"
      :is-loading="isCancelling"
      @confirm="confirmCancel"
      @cancel="cancelCancel"
    />
    <h2>Rental Search</h2>
    
    <div class="search-container">
      <div class="search-box">
        <input 
          type="email" 
          v-model="email" 
          placeholder="Enter your email to search rentals"
          class="search-input"
          @keyup.enter="searchRentals"
        >
        <button @click="searchRentals" class="search-btn">
          <i class="fas fa-search"></i> Search
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">Loading rentals...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="searched && rentals.length === 0" class="no-results">
      No rentals found for this email
    </div>
    
    <div v-else class="list-grid">
      <div v-for="rental in rentals" :key="rental.id" class="list-card">
        <div class="list-header">
          <h3>{{ rental.car.name }} {{ rental.car.model }}</h3>
          <span :class="['status', rental.status.toLowerCase()]">
            {{ rental.status }}
          </span>
        </div>
        
        <div class="details">
          <div class="detail">
            <span class="label">Customer:</span>
            <span class="value">{{ rental.customerName }}</span>
          </div>
          <div class="detail">
            <span class="label">Email:</span>
            <span class="value">{{ rental.customerEmail }}</span>
          </div>
          <div class="detail">
            <span class="label">Period:</span>
            <span class="value">
              {{ formatDate(rental.startDate) }} to {{ formatDate(rental.endDate) }}
              ({{ calculateDays(rental.startDate, rental.endDate) }} days)
            </span>
          </div>
          <div class="detail">
            <span class="label">Total Price:</span>
            <span class="value price">${{ rental.totalPrice.toFixed(2) }}</span>
          </div>
        </div>
        
        <div class="actions">
          <button 
            v-if="rental.status === 'PENDING'" 
            @click="cancelRental(rental)"
            class="btn-cancel"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import rentalService from '@/services/rentalService';
import ConfirmationDialog from '@/components/ConfirmationDialog.vue';

export default {
  name: 'RentalList',
  components: {
    ConfirmationDialog,
  },
  data() {
    return {
      email: '',
      rentals: [],
      loading: false,
      error: null,
      searched: false,
      searchTimeout: null,
      showConfirmDialog: false,
      isCancelling: false,
      selectedRental: null
    };
  },
  methods: {
    async searchRentals() {
      if (!this.email) {
        this.error = 'Please enter an email address';
        return;
      }
      
      this.loading = true;
      this.error = null;
      this.searched = true;
      
      try {
        const response = await fetch(`/api/rentals/email/${encodeURIComponent(this.email)}`);
        if (!response.ok) {
          throw new Error('Failed to fetch rentals');
        }
        this.rentals = await response.json();
      } catch (err) {
        console.error('Error fetching rentals:', err);
        this.error = 'Failed to load rentals. Please try again.';
        this.rentals = [];
      } finally {
        this.loading = false;
      }
    },
    
    cancelRental(rental) {
      if (rental.status !== 'PENDING') {
        this.$toast.error('Only pending rentals can be cancelled');
        return;
      }
      this.selectedRental = rental;
      this.showConfirmDialog = true;
    },
    
    async confirmCancel() {
      if (!this.selectedRental) return;
      
      this.isCancelling = true;
      
      try {
        await rentalService.cancelRental(this.selectedRental.id);
        // Update local rental status
        this.selectedRental.status = 'CANCELLED';
        this.$toast.success('Rental cancelled successfully');
      } catch (err) {
        console.error('Error cancelling rental:', err);
        this.$toast.error('Failed to cancel rental');
      } finally {
        this.isCancelling = false;
        this.showConfirmDialog = false;
        this.selectedRental = null;
      }
    },
    
    cancelCancel() {
      this.showConfirmDialog = false;
      this.selectedRental = null;
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
    
    calculateDays(startDate, endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      return Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
    }
  }
};
</script>

<style scoped>
@import '@/assets/styles/list-styles.css';
</style>
