import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useExchangeStore = defineStore('exchange', () => {
  const changeMoney = ref([])
  const countries = [
    '아랍에미리트 디르함',
    '호주 달러',
    '바레인 디나르',
    '브루나이 달러',
    '캐나다 달러',
    '스위스 프랑',
    '위안화',
    '덴마아크 크로네',
    '유로',
    '영국 파운드',
    '홍콩 달러',
    '인도네시아 루피아',
    '일본 옌',
    '쿠웨이트 디나르',
    '말레이지아 링기트',
    '노르웨이 크로네',
    '뉴질랜드 달러',
    '사우디 리얄',
    '스웨덴 크로나',
    '싱가포르 달러',
    '태국 바트',
    '미국 달러'
  ]

  const countryCodes = {
    '아랍에미리트 디르함': 'AED',
    '호주 달러': 'AUD',
    '바레인 디나르': 'BHD',
    '브루나이 달러': 'BND',
    '캐나다 달러': 'CAD',
    '스위스 프랑': 'CHF',
    '위안화': 'CNH',
    '덴마아크 크로네': 'DKK',
    '유로': 'EUR',
    '영국 파운드': 'GBP',
    '홍콩 달러': 'HKD',
    '인도네시아 루피아': 'IDR(100)',
    '일본 옌': 'JPY(100)',
    '쿠웨이트 디나르': 'KWD',
    '말레이지아 링기트': 'MYR',
    '노르웨이 크로네': 'NOK',
    '뉴질랜드 달러': 'NZD',
    '사우디 리얄': 'SAR',
    '스웨덴 크로나': 'SEK',
    '싱가포르 달러': 'SGD',
    '태국 바트': 'THB',
    '미국 달러': 'USD'
  }

  const getChange = function (data) {
    changeMoney.value = data
  }

  return { countries, getChange, changeMoney, countryCodes }
}, { persist: true })
