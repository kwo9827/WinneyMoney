import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const usePortfolioStore = defineStore('portfolio', () => {
  const portfolios = ref([])

  const getPortfolios = function (data) {
    console.log('스토어에서 받음', data)
    portfolios.value = data
  }
  return { portfolios, getPortfolios }
}, { persist: true })
