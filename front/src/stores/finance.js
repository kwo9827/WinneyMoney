import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', () => {
  const deposits = ref([])
  const savings = ref([])

  // 예금 데이터 가져오기
  const fetchDeposits = function () {
    const API_URL = 'http://127.0.0.1:8000/finlife/deposit-products/'
    axios.get(API_URL)
      .then((res) => {
        console.log('예금 데이터 가져오기 성공:', res.data)
        deposits.value = res.data
      })
      .catch((err) => {
        console.error('예금 데이터 가져오기 실패:', err)
      })
  }

  // 적금 데이터 가져오기
  const fetchSavings = function () {
    const API_URL = 'http://127.0.0.1:8000/finlife/saving-products/'
    axios.get(API_URL)
      .then((res) => {
        console.log('적금 데이터 가져오기 성공:', res.data)
        savings.value = res.data
      })
      .catch((err) => {
        console.error('적금 데이터 가져오기 실패:', err)
      })
  }

  return { deposits, savings, fetchDeposits, fetchSavings }
})
