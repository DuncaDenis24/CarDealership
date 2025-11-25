<template>
  <div class="list-container">
    <ConfirmationDialog
      :is-open="showConfirmDialog"
      title="Confirm Cancellation"
      :message="'Are you sure you want to cancel the purchase for ' + (selectedPurchase ? getCarName(selectedPurchase) : 'this car') + '?'"
      confirm-text="Yes, Cancel Purchase"
      :is-loading="isCancelling"
      @confirm="confirmCancel"
      @cancel="cancelCancel"
    />
    <h2>Purchase Search</h2>
    
    <div class="search-container">
      <div class="search-box">
        <input 
          type="email" 
          v-model="email" 
          placeholder="Enter your email to search purchases"
          class="search-input"
          @keyup.enter="searchPurchases"
        >
        <button @click="searchPurchases" class="search-btn">
          <i class="fas fa-search"></i> Search
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">Loading purchases...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="searched && purchases.length === 0" class="no-results">
      No purchases found for this email
    </div>
    
    <div v-else class="list-grid">
      <div v-for="purchase in purchases" :key="purchase.id" class="list-card">
        <div class="list-header">
          <h3>{{ getCarName(purchase) }}</h3>
          <span :class="['status', purchase.status.toLowerCase()]">
            {{ purchase.status }}
          </span>
        </div>
        
        <div class="details">
          <div class="detail">
            <span class="label">Customer:</span>
            <span class="value">{{ purchase.customerName || 'N/A' }}</span>
          </div>
          <div class="detail">
            <span class="label">Email:</span>
            <span class="value">{{ purchase.customerEmail || 'N/A' }}</span>
          </div>
          <div class="detail">
            <span class="label">Purchase Date:</span>
            <span class="value">{{ formatDate(purchase.purchaseDate) }}</span>
          </div>
          <div class="detail">
            <span class="label">Total Price:</span>
            <span class="value price">${{ getPrice(purchase) }}</span>
          </div>
        </div>
        
        <div class="actions">
          <button 
            v-if="purchase.status === 'PENDING'" 
            @click="cancelPurchase(purchase)"
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
import purchaseService from '@/services/purchaseService';
import ConfirmationDialog from '@/components/ConfirmationDialog.vue';

export default {
  name: 'PurchaseList',
  components: {
    ConfirmationDialog,
  },
  data() {
    return {
      email: '',
      purchases: [],
      loading: false,
      error: null,
      searched: false,
      searchTimeout: null,
      showConfirmDialog: false,
      isCancelling: false,
      selectedPurchase: null
    };
  },
  methods: {
    getCarName(purchase) {
      if (!purchase) return 'Car';
      if (purchase.car?.name && purchase.car?.model) {
        return `${purchase.car.name} ${purchase.car.model}`;
      }
      return 'Car';
    },
    
    getPrice(purchase) {
      if (!purchase || purchase.purchasePrice === undefined || purchase.purchasePrice === null) return '0.00';
      return Number(purchase.purchasePrice).toFixed(2);
    },
    async searchPurchases() {
      if (!this.email) {
        this.error = 'Please enter an email address';
        return;
      }
      
      this.loading = true;
      this.error = null;
      this.searched = true;
      
      try {
        // Use the purchaseService to fetch purchases by email
        const response = await purchaseService.getPurchasesByEmail(this.email);
        console.log('API Response:', response);
        this.purchases = Array.isArray(response) ? response : [response];
        console.log('Processed purchases:', this.purchases);
      } catch (err) {
        console.error('Error fetching purchases:', err);
        this.error = err.response?.data?.message || 'Failed to load purchases. Please try again.';
        this.purchases = [];
      } finally {
        this.loading = false;
      }
    },
    
    cancelPurchase(purchase) {
      if (purchase.status !== 'PENDING') {
        this.$toast.error('Only pending purchases can be cancelled');
        return;
      }
      this.selectedPurchase = purchase;
      this.showConfirmDialog = true;
    },
    
    async confirmCancel() {
      if (!this.selectedPurchase) return;
      
      this.isCancelling = true;
      
      try {
        await purchaseService.cancelPurchase(this.selectedPurchase.id);
        // Update local state
        this.selectedPurchase.status = 'CANCELLED';
        this.$toast.success('Purchase cancelled successfully');
      } catch (error) {
        console.error('Error cancelling purchase:', error);
        this.$toast.error('Failed to cancel purchase. Please try again.');
      } finally {
        this.isCancelling = false;
        this.showConfirmDialog = false;
        this.selectedPurchase = null;
      }
    },
    
    cancelCancel() {
      this.showConfirmDialog = false;
      this.selectedPurchase = null;
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    }
  }
};
</script>

<style scoped>
@import '@/assets/styles/list-styles.css';
</style>
