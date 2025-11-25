<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App'
});
</script>

<style>
/* Base styles */
:root {
  --primary: #4a6cf7;
  --primary-dark: #2541b2;
  --danger: #ff4d4f;
  --danger-dark: #f5222d;
  --white: #ffffff;
  --gray-100: #f8f9fa;
  --gray-200: #e9ecef;
  --gray-500: #adb5bd;
  --gray-800: #343a40;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 12px rgba(0, 0, 0,0.15);
  --radius: 8px;
  --transition: all 0.3s ease;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.5;
  color: var(--gray-800);
  background-color: var(--gray-100);
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}


/* Base styles */
:root {
  --primary-color: #42b983;
  --primary-dark: #369b6b;
  --secondary-color: #2c3e50;
  --light-gray: #f8f9fa;
  --dark-gray: #343a40;
  --text-color: #2c3e50;
  --text-light: #6c757d;
  --border-color: #dee2e6;
  --success: #28a745;
  --danger: #dc3545;
  --warning: #ffc107;
  --info: #17a2b8;
  --white: #ffffff;
  --box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  position: relative;
}

body {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-color);
  line-height: 1.6;
  background-color: var(--light-gray);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

#app {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.router-view-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Utility classes */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.btn {
  display: inline-block;
  font-weight: 500;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  user-select: none;
  border: 1px solid transparent;
  padding: 0.5rem 1.25rem;
  font-size: 1rem;
  line-height: 1.5;
  border-radius: 4px;
  transition: var(--transition);
  cursor: pointer;
  text-decoration: none;
}

.btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.btn-primary {
  color: var(--white);
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-dark);
  border-color: var(--primary-dark);
}

.btn-outline {
  color: var(--primary-color);
  background-color: transparent;
  border: 1px solid var(--primary-color);
}

.btn-outline:hover:not(:disabled) {
  color: var(--white);
  background-color: var(--primary-color);
}

.btn-danger {
  color: var(--white);
  background-color: var(--danger);
  border-color: var(--danger);
}

.btn-danger:hover:not(:disabled) {
  background-color: #c82333;
  border-color: #bd2130;
}

.text-center {
  text-align: center;
}

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }
.mt-5 { margin-top: 3rem; }

.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }
.mb-5 { margin-bottom: 3rem; }

/* Card styles */
.card {
  background: var(--white);
  border-radius: 8px;
  box-shadow: var(--box-shadow);
  overflow: hidden;
  transition: var(--transition);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-body {
  padding: 1.5rem;
}

.card-title {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--secondary-color);
}

/* Form styles */
.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-control {
  display: block;
  width: 100%;
  padding: 0.5rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--text-color);
  background-color: var(--white);
  background-clip: padding-box;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  border-color: var(--primary-color);
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(66, 185, 131, 0.25);
}

/* Alert styles */
.alert {
  position: relative;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 4px;
}

.alert-success {
  color: #155724;
  background-color: #d4edda;
  border-color: #c3e6cb;
}

.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

.alert-info {
  color: #0c5460;
  background-color: #d1ecf1;
  border-color: #bee5eb;
}

/* Animation for page transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive images */
.img-fluid {
  max-width: 100%;
  height: auto;
}

/* Responsive utilities */
@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .btn {
    padding: 0.4rem 1rem;
    font-size: 0.9rem;
  }
}
</style>