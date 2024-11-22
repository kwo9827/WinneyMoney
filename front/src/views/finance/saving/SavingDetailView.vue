<template>
  <div class="container">
    <h1>{{ saving.kor_co_nm }} - {{ saving.fin_prdt_nm }}</h1>
    <p>기간별 금리:</p>
    <ul>
      <li v-for="option in saving.options" :key="option.save_trm">
        {{ option.save_trm }}개월: {{ option.intr_rate }}%
      </li>
    </ul>
    <router-link :to="{name: 'SavingView' }">목록으로 돌아가기</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAccountStore } from '@/stores/accounts';
import axios from 'axios';
import { RouterLink } from 'vue-router';

const store = useAccountStore()
const saving = ref({});
const route = useRoute()
const router = useRouter()
const API_URL = store.API_URL

onMounted(() => {
  const product_id = route.params.product_id; // URL에서 id 가져오기
  axios({
    method: 'get',
    url: `${API_URL}/finlife/saving-products/detail/${product_id}/`
  })
    .then(res => {
      console.log('성공')
      saving.value = res.data; // API 응답 데이터 저장
    })
    .catch(err => {
      console.error('API 호출 오류:', err);
    });
});
</script>

<style scoped>
.container {
  padding: 2rem;
}
</style>
