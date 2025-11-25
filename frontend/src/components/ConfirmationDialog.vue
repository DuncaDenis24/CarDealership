<template>
  <div v-if="isOpen" class="confirmation-overlay">
    <div class="confirmation-dialog">
      <div class="confirmation-header">
        <h3>{{ title }}</h3>
      </div>
      <div class="confirmation-body">
        <p>{{ message }}</p>
      </div>
      <div class="confirmation-footer">
        <button 
          @click="onCancel" 
          :disabled="isLoading" 
          class="btn-cancel"
        >
          Cancel
        </button>
        <button 
          @click="onConfirm" 
          :disabled="isLoading" 
          class="btn-confirm"
        >
          <span v-if="!isLoading">{{ confirmText }}</span>
          <span v-else class="loading-spinner"></span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmationDialog',
  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: 'Confirm Action'
    },
    message: {
      type: String,
      required: true
    },
    confirmText: {
      type: String,
      default: 'Confirm'
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    onConfirm() {
      this.$emit('confirm');
    },
    onCancel() {
      this.$emit('cancel');
    }
  }
};
</script>

<style scoped>
.confirmation-overlay {
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

.confirmation-dialog {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  animation: fadeIn 0.2s ease-out;
}

.confirmation-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eaeaea;
  background-color: #f8f9fa;
}

.confirmation-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.confirmation-body {
  padding: 20px;
  color: #34495e;
  line-height: 1.5;
}

.confirmation-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  background-color: #f8f9fa;
  border-top: 1px solid #eaeaea;
}

button {
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: #f1f3f5;
  color: #495057;
}

.btn-cancel:hover:not(:disabled) {
  background-color: #e9ecef;
}

.btn-confirm {
  background-color: #e74c3c;
  color: white;
  min-width: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-confirm:not(:disabled):hover {
  background-color: #c0392b;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
