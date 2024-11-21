import { createRouter, createWebHistory } from 'vue-router'

// Views
import HomeView from '@/views/HomeView.vue'

// account 기능
import ChangePasswordView from '@/views/accounts/ChangePasswordView.vue'
import FindPasswordView from '@/views/accounts/FindPasswordView.vue'
import LogInView from '@/views/accounts/LogInView.vue'
import ProfileView from '@/views/accounts/ProfileView.vue'
import SignUpView from '@/views/accounts/SignUpView.vue'
import EditProfileView from '@/views/accounts/EditProfileView.vue'

// 게시글 기능
import ArticleView from '@/views/articles/ArticleView.vue'
import CreateView from '@/views/articles/CreateView.vue'
import DetailView from '@/views/articles/DetailView.vue'
import UpdateView from '@/views/articles/UpdateView.vue'

// etc 기능
import MapView from '@/views/etc/MapView.vue'
import ExchangeView from '@/views/etc/ExchangeView.vue'
import NewsHomeView from '@/views/etc/NewsHomeView.vue'
import NotFoundView from '@/views/etc/NotFoundView.vue'

// finance 기능
import CartView from '@/views/finance/CartView.vue'
import InterestDetailView from '@/views/finance/InterestDetailView.vue'
import InterestView from '@/views/finance/InterestView.vue'
import { useAccountStore } from '@/stores/accounts'

// 라우터 설정
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 홈 화면
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
    },
    // 로그인
    {
      path: '/accounts/auth/logIn',
      name: 'LogInView',
      component: LogInView,
    },
    // 회원가입
    {
      path: '/accounts/auth/signup',
      name: 'SignUpView',
      component: SignUpView,
    },
    // 비밀번호 찾기
    {
      path: '/accounts/auth/password/reset',
      name: 'FindPasswordView',
      component: FindPasswordView,
    },
    // 비밀번호 변경
    {
      path: '/accounts/auth/password/change',
      name: 'ChangePasswordView',
      component: ChangePasswordView,
    },
    // 프로필
    {
      path: '/profile',
      name: 'ProfileView',
      component: ProfileView,
    },
    // 회원 정보 수정
    {
      path: '/accounts/edit/',
      name: 'EditProfileView',
      component: EditProfileView,
    },
    // 게시판 목록 및 작성
    {
      path: '/articles',
      name: 'ArticleView',
      component: ArticleView,
    },
    // 게시글 수정
    {
      path: '/articles/:id/edit',
      name: 'UpdateView',
      component: UpdateView,
    },
    // 게시글 상세
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView,
    },
    // 새 글 작성
    {
      path: '/articles/create',
      name: 'CreateView',
      component: CreateView,
    },
    // 지도
    {
      path: '/map',
      name: 'MapView',
      component: MapView,
    },
    // 환전
    {
      path: '/exchange',
      name: 'ExchangeView',
      component: ExchangeView,
    },
    // 뉴스
    {
      path: '/news',
      name: 'NewsHomeView',
      component: NewsHomeView,
    },
    // 장바구니
    {
      path: '/cart',
      name: 'CartView',
      component: CartView,
    },
    // 상품 상세
    {
      path: '/interest-detail',
      name: 'InterestDetailView',
      component: InterestDetailView,
    },
    // 상품
    {
      path: '/interest',
      name: 'InterestView',
      component: InterestView,
    },
    // 추천 시스템
    {
      path: '/algorithm',
      name: 'AlgorithmView',
      component: () => import('@/views/etc/AlgorithmView.vue'),
    },
    // Not Found
    {
      path: '/:catchAll(.*)',
      name: 'NotFoundView',
      component: NotFoundView,
    },
  ],
})

// 기본 라우팅 가드
router.beforeEach((to, from) => {
  const store = useAccountStore()
  const publicPages = ['HomeView', 'ArticleView', 'DetailView', 'LogInView', 'SignUpView']
  const authRequired = !publicPages.includes(to.name)

  if (authRequired && !store.isLogin) {
    window.alert('로그인이 필요한 서비스입니다.')
    return { name: 'LogInView' }
  }

  if ((to.name === 'SignUpView' || to.name === 'LogInView') && store.isLogin) {
    window.alert('이미 로그인 되어있습니다.')
    return { name: 'ArticleView' }
  }
})

export default router
