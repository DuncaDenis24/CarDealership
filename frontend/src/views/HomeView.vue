<template>
  <div class="home">
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1>Welcome to CarDealer</h1>
          <p class="lead">Find your perfect car for rent or purchase</p>
          <div class="cta-buttons">
            <router-link to="/cars" class="btn btn-primary btn-lg me-3">
              <i class="fas fa-car me-2"></i>Browse Cars
            </router-link>
            <router-link to="/rentals" class="btn btn-outline-light btn-lg">
              <i class="fas fa-calendar-alt me-2"></i>My Rentals
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <section class="features-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">Why Choose Us</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="feature-card text-center p-4 h-100">
              <div class="icon-wrapper mb-3">
                <i class="fas fa-shield-alt fa-3x text-primary"></i>
              </div>
              <h3>Safe & Secure</h3>
              <p>All our vehicles are thoroughly inspected and maintained to the highest standards.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card text-center p-4 h-100">
              <div class="icon-wrapper mb-3">
                <i class="fas fa-tag fa-3x text-primary"></i>
              </div>
              <h3>Best Prices</h3>
              <p>Competitive pricing and special offers to make your rental or purchase affordable.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card text-center p-4 h-100">
              <div class="icon-wrapper mb-3">
                <i class="fas fa-headset fa-3x text-primary"></i>
              </div>
              <h3>24/7 Support</h3>
              <p>Our customer service team is available around the clock to assist you.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="how-it-works py-5 bg-light">
      <div class="container">
        <h2 class="text-center mb-5">How It Works</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="step-card text-center p-4">
              <div class="step-number">1</div>
              <h3>Choose Your Car</h3>
              <p>Browse our wide selection of vehicles and pick the one that suits your needs.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="step-card text-center p-4">
              <div class="step-number">2</div>
              <h3>Make a Reservation</h3>
              <p>Select your dates and complete the booking process in just a few clicks.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="step-card text-center p-4">
              <div class="step-number">3</div>
              <h3>Enjoy Your Ride</h3>
              <p>Pick up your car and enjoy your journey with peace of mind.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  metaInfo: {
    title: 'Home - CarDealer',
    meta: [
      { name: 'description', content: 'Find and book your perfect car for rent or purchase at CarDealer. Best prices and great service guaranteed!' }
    ]
  }
};
</script>

<style scoped>
.hero-section {
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
              url('https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
  background-size: cover;
  background-position: center;
  color: white;
  padding: 8rem 0;
  text-align: center;
  margin-bottom: 3rem;
}

.hero-content h1 {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.hero-content .lead {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.cta-buttons {
  margin-top: 2rem;
}

.feature-card, .step-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
}

.feature-card:hover, .step-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(66, 185, 131, 0.1);
  border-radius: 50%;
}

.step-number {
  width: 50px;
  height: 50px;
  background-color: var(--primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 1.5rem;
}

.how-it-works {
  background-color: #f8f9fa;
}

/* Responsive styles */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2.5rem;
  }
  
  .hero-content .lead {
    font-size: 1.25rem;
  }
  
  .cta-buttons .btn {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
  }
  
  .cta-buttons .btn:last-child {
    margin-bottom: 0;
  }
}
</style>
