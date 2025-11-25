<template>
  <footer class="app-footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>CarDealer</h3>
          <p>Your trusted partner for car rentals and purchases.</p>
          <div class="social-links">
            <a href="#" aria-label="Facebook"><i class="fab fa-facebook"></i></a>
            <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
            <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
          </div>
        </div>
        
        <div class="footer-section">
          <h4>Quick Links</h4>
          <ul>
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/rentals">My Rentals</router-link></li>
            <li><router-link to="/purchases">My Purchases</router-link></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4>Contact Us</h4>
          <p><i class="fas fa-envelope"></i> contact@cardealer.com</p>
          <p><i class="fas fa-phone"></i> +1 234 567 890</p>
          <p><i class="fas fa-map-marker-alt"></i> 123 Car Street, Auto City</p>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; {{ currentYear }} CarDealer. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
  data() {
    return {
      currentYear: new Date().getFullYear()
    };
  }
};
</script>

<style scoped>
.app-footer {
  background-color: #2c3e50;
  color: #ecf0f1;
  padding: 3rem 0 1rem;
  margin-top: 3rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h3,
.footer-section h4 {
  color: #42b983;
  margin-top: 0;
  margin-bottom: 1.25rem;
  font-size: 1.25rem;
}

.footer-section p {
  margin: 0.5rem 0;
  line-height: 1.6;
  color: #bdc3c7;
}

.social-links {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.social-links a {
  color: #bdc3c7;
  font-size: 1.25rem;
  transition: color 0.3s;
}

.social-links a:hover {
  color: #42b983;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section ul li {
  margin-bottom: 0.75rem;
}

.footer-section a {
  color: #bdc3c7;
  text-decoration: none;
  transition: color 0.3s;
  display: inline-block;
}

.footer-section a:hover {
  color: #42b983;
}

.footer-section i {
  margin-right: 0.5rem;
  width: 20px;
  text-align: center;
  color: #42b983;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 1.5rem;
  text-align: center;
  color: #7f8c8d;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
  
  .footer-section {
    text-align: center;
  }
  
  .social-links {
    justify-content: center;
  }
}
</style>
