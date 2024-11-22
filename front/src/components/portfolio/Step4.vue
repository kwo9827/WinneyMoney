<template>
  <div>
    <label for="investment">초기 투자 금액:</label>
    <input id="investment" v-model.number="portfolio.totalInvestment" type="number" />
    <button @click="$emit('next')">다음</button>
  </div>
</template>

<script setup>
import { usePortfolioStore } from "@/stores/portfolio";

const portfolio = usePortfolioStore().portfolio;
</script>
