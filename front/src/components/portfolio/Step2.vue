<template>
  <div>
    <label for="economy">경제 전망:</label>
    <select id="economy" v-model="portfolio.predictedEconomy">
      <option value="growth">성장</option>
      <option value="recession">하락</option>
      <option value="stability">유지</option>
    </select>
    <button @click="$emit('next')">다음</button>
  </div>
</template>

<script setup>
import { usePortfolioStore } from "@/stores/portfolio";

const portfolio = usePortfolioStore().portfolio;
</script>
