import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '@/layouts/MainLayout.vue';

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/HomeView.vue')
      },
      {
        path: 'cars',
        name: 'Cars',
        component: () => import('@/views/CarList.vue')
      },
      {
        path: 'rent-car/:carId',
        name: 'RentCar',
        component: () => import('@/views/RentalForm.vue'),
        props: true
      },
      {
        path: 'rentals',
        name: 'Rentals',
        component: () => import('@/views/RentalList.vue')
      },
      {
        path: 'buy-car/:carId',
        name: 'BuyCar',
        component: () => import('@/views/PurchaseForm.vue'),
        props: true
      },
      {
        path: 'purchases',
        name: 'Purchases',
        component: () => import('@/views/PurchaseList.vue')
      },
      {
        path: '/:pathMatch(.*)*',
        redirect: '/'
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

export default router;
