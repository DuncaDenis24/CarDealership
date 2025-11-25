<template>
  <div class="app-layout">
    <NavBar />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import NavBar from '@/components/NavBar.vue';
import AppFooter from '@/components/AppFooter.vue';

export default defineComponent({
  name: 'MainLayout',
  components: {
    NavBar,
    AppFooter
  }
});
</script>

<style scoped>
:global(html, body) {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100%;
}

.app-layout {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 0;
  padding: 0;
}

.main-content {
  flex: 1;
  width: 100%;
  padding: 2rem 0;
  background-color: #f8f9fa;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

/* Remove the max-width constraint from all children */
.main-content > * {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0 1.5rem;
}

/* Global transition styles */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive padding */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem 0;
  }
}
</style>
