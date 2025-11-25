<template>
  <nav class="navbar">
    <div class="container">
      <router-link to="/" class="logo">
        <h1>CarDealer</h1>
      </router-link>
      
      <button 
        class="mobile-menu-button"
        @click="isMenuOpen = !isMenuOpen"
        aria-label="Toggle menu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
      
      <div class="nav-links" :class="{ 'active': isMenuOpen }">
        <router-link to="/" @click="isMenuOpen = false" class="nav-link">
          <i class="fas fa-car"></i> Available Cars
        </router-link>
        <router-link to="/rentals" @click="isMenuOpen = false" class="nav-link">
          <i class="fas fa-calendar-alt"></i> My Rentals
        </router-link>
        <router-link to="/purchases" @click="isMenuOpen = false" class="nav-link">
          <i class="fas fa-receipt"></i> My Purchases
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      isMenuOpen: false
    };
  },
  watch: {
    $route() {
      this.isMenuOpen = false;
    }
  }
};
</script>

<style scoped>
.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.logo {
  text-decoration: none;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  transition: all 0.3s ease;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #42b983;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #42b983;
  border-radius: 2px;
}

.mobile-menu-button {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  z-index: 1001;
}

.mobile-menu-button span {
  display: block;
  width: 24px;
  height: 2px;
  background-color: white;
  margin: 5px 0;
  transition: all 0.3s ease;
}

/* Mobile styles */
@media (max-width: 768px) {
  .mobile-menu-button {
    display: block;
  }
  
  .nav-links {
    position: fixed;
    top: 0;
    right: -100%;
    width: 70%;
    height: 100vh;
    background-color: #2c3e50;
    flex-direction: column;
    padding: 5rem 2rem 2rem;
    box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .nav-links.active {
    right: 0;
  }
  
  .nav-link {
    padding: 1rem 0;
    font-size: 1.1rem;
  }
  
  .mobile-menu-button.active span:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
  }
  
  .mobile-menu-button.active span:nth-child(2) {
    opacity: 0;
  }
  
  .mobile-menu-button.active span:nth-child(3) {
    transform: rotate(-45deg) translate(7px, -6px);
  }
}
</style>
