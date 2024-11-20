import { createRouter, createWebHistory } from 'vue-router';

// accounts
import ChangePasswordView from '@/views/accounts/ChangePasswordView.vue';
import FindPasswordView from '@/views/accounts/FindPasswordView.vue';
import LoginView from '@/views/accounts/LoginView.vue';
import ProfileView from '@/views/accounts/ProfileView.vue';
import SignUpView from '@/views/accounts/SignUpView.vue';
import UpdateView from '@/views/accounts/UpdateView.vue';

// articles
import ArticleView from '@/views/articles/ArticleView.vue';
import CreateView from '@/views/articles/CreateView.vue';
import DetailView from '@/views/articles/DetailView.vue';

// finance
import CartView from '@/views/finance/CartView.vue';
import InterestDetailView from '@/views/finance/InterestDetailView.vue';
import InterestView from '@/views/finance/InterestView.vue';

// etc
import ExchangeView from '@/views/etc/ExchangeView.vue';
import MapView from '@/views/etc/MapView.vue';

// home
import HomeView from '@/views/HomeView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Home
    { path: '/', name: 'HomeView', component: HomeView },

    // Accounts
    { path: '/accounts/signup', name: 'SignUpView', component: SignUpView },
    { path: '/accounts/login', name: 'LoginView', component: LoginView },
    { path: '/accounts/profile', name: 'ProfileView', component: ProfileView },
    { path: '/accounts/update', name: 'UpdateView', component: UpdateView },
    { path: '/accounts/change-password', name: 'ChangePasswordView', component: ChangePasswordView },
    { path: '/accounts/find-password', name: 'FindPasswordView', component: FindPasswordView },

    // Articles
    { path: '/articles', name: 'ArticleView', component: ArticleView },
    { path: '/articles/create', name: 'CreateView', component: CreateView },
    { path: '/articles/:id', name: 'DetailView', component: DetailView, props: true },

    // Finance
    { path: '/finance/cart', name: 'CartView', component: CartView },
    { path: '/finance/interest', name: 'InterestView', component: InterestView },
    { path: '/finance/interest/:id', name: 'InterestDetailView', component: InterestDetailView, props: true },

    // Etc
    { path: '/etc/exchange', name: 'ExchangeView', component: ExchangeView },
    { path: '/etc/map', name: 'MapView', component: MapView },

    // 404 Not Found
    { path: '/:catchAll(.*)', name: 'NotFound', component: () => import('@/views/etc/NotFoundView.vue') },
  ],
});

// 인증 가드
router.beforeEach((to, from) => {
  const publicPages = ['HomeView', 'ArticleView', 'DetailView', 'LoginView', 'SignUpView'];
  const authRequired = !publicPages.includes(to.name);
  const isAuthenticated = !!localStorage.getItem('token');

  if (authRequired && !isAuthenticated) {
    window.alert('로그인이 필요한 서비스입니다.');
    return { name: 'LoginView' };
  }

  if ((to.name === 'SignUpView' || to.name === 'LoginView') && isAuthenticated) {
    window.alert('이미 로그인 되어있습니다.');
    return { name: 'ArticleView' };
  }
});

export default router;
