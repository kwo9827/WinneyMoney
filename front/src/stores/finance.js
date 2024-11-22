import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useFinanceStore = defineStore('finance', () => {
  const deposits = ref([])
  const savings = ref([])

  const getDeposit = function (data) {
    console.log('스토어에서 받음', data)
    deposits.value = data
  }

  const getSavings = function (data) {
    console.log('스토어에서 받음', data)
    savings.value = data
  }
  return { getDeposit, getSavings, deposits, savings }
}, { persist: true })
