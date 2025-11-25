import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import './assets/main.css';

// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import 'bootstrap';

// Import Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

// Add all icons to the library
library.add(fas);

const app = createApp(App);

// Use plugins
app.use(createPinia());
app.use(router);

// Register global components
app.component('font-awesome-icon', FontAwesomeIcon);

// Mount the app
app.mount('#app');

// Global error handler
app.config.errorHandler = (err) => {
  console.error('Vue error:', err);
};

// Global properties
app.config.globalProperties.$filters = {
  formatCurrency(value) {
    return new Intl.NumberFormat('ro-RO', {
      style: 'currency',
      currency: 'RON'
    }).format(value);
  },
  formatDate(date) {
    return new Date(date).toLocaleDateString('ro-RO');
  }
};