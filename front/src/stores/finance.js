import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './accounts'

export const useFinanceStore = defineStore('finance', () => {
  const deposits = ref([]) // 예금 리스트
  const savings = ref([]) // 적금 리스트

  const favoriteDeposits = ref([]) // 즐겨찾기된 예금 리스트
  const favoriteSavings = ref([]) // 즐겨찾기된 적금 리스트

  const accountStore = useAccountStore()

  // 예금 데이터 가져오기
  const fetchDeposits = function () {
    const API_URL = 'http://127.0.0.1:8000/finlife/deposit-products/'
    axios
      .get(API_URL)
      .then((res) => {
        console.log('예금 데이터 가져오기 성공:', res.data)
        res.data.forEach((item) => {
          // 중복 확인 후 데이터 추가
          if (!deposits.value.some((deposit) => deposit.id === item.id)) {
            deposits.value.push(item)
          }
        })
      })
      .catch((err) => {
        console.error('예금 데이터 가져오기 실패:', err)
      })
  }

  // 적금 데이터 가져오기
  const fetchSavings = function () {
    const API_URL = 'http://127.0.0.1:8000/finlife/saving-products/'
    axios
      .get(API_URL)
      .then((res) => {
        console.log('적금 데이터 가져오기 성공:', res.data)
        res.data.forEach((item) => {
          // 중복 확인 후 데이터 추가
          if (!savings.value.some((saving) => saving.id === item.id)) {
            savings.value.push(item)
          }
        })
      })
      .catch((err) => {
        console.error('적금 데이터 가져오기 실패:', err)
      })
  }

  // 즐겨찾기 데이터 가져오기
  const fetchFavorites = function () {
    const API_URL = 'http://127.0.0.1:8000/finlife/favorites/'
    const headers = {
      Authorization: `Token ${accountStore.token}`
    }
    axios
      .get(API_URL, { headers })
      .then((res) => {
        console.log('즐겨찾기 데이터 가져오기 성공:', res.data)
        favoriteDeposits.value = res.data.favorite_deposit
        favoriteSavings.value = res.data.favorite_saving
      })
      .catch((err) => {
        console.error('즐겨찾기 데이터 가져오기 실패:', err)
      })
  }

  // 즐겨찾기(예금)
  const toggleFavoriteDeposit = function (fin_prdt_cd) {
    console.log('토큰 값 확인:', accountStore.token);
    const API_URL = `http://127.0.0.1:8000/finlife/favorites/deposit/${fin_prdt_cd}/`;
    const headers = {
      Authorization: `Token ${accountStore.token}`, // 인증 토큰 추가
    };
    axios
      .post(API_URL, {}, { headers }) // 인증 헤더 포함
      .then((response) => {
        console.log('응답 메시지:', response.data.message)
        // 즐겨찾기 리스트 새로고침
        fetchFavorites();
      })
      .catch((err) => {
        console.error('예금 즐겨찾기 실패:', err.response || err);
        alert('즐겨찾기 작업 중 오류가 발생했습니다.');
      });
  };


// 즐겨찾기(적금)
const toggleFavoriteSaving = function (fin_prdt_cd) {
  console.log('토큰 값 확인:', accountStore.token);
  const API_URL = `http://127.0.0.1:8000/finlife/favorites/saving/${fin_prdt_cd}/`;
  const headers = {
    Authorization: `Token ${accountStore.token}`, // 인증 토큰 추가
  };
  axios
    .post(API_URL, {}, { headers }) // 인증 헤더 포함
    .then((response) => {
      console.log('응답 메시지:', response.data.message);
      // 즐겨찾기 리스트 새로고침
      fetchFavorites();
    })
    .catch((err) => {
      console.error('적금 즐겨찾기 실패:', err.response || err);
      alert('적금 즐겨찾기 작업 중 오류가 발생했습니다.');
    });
};


  return {
    deposits,
    savings,
    favoriteDeposits,
    favoriteSavings,
    fetchDeposits,
    fetchSavings,
    fetchFavorites,
    toggleFavoriteDeposit,
    toggleFavoriteSaving,
  }
})
