<template>
  <div>
    <label>위험 성향:</label>
    <div>
      <input type="radio" id="low" value="low" v-model="portfolio.riskPreference" />
      <label for="low">수비적</label>
    </div>
    <div>
      <input type="radio" id="medium" value="medium" v-model="portfolio.riskPreference" />
      <label for="medium">보통</label>
    </div>
    <div>
      <input type="radio" id="high" value="high" v-model="portfolio.riskPreference" />
      <label for="high">공격형</label>
    </div>
    <button @click="$emit('next')">다음</button>
  </div>
</template>

<script setup>
import { usePortfolioStore } from "@/stores/portfolio";

const portfolio = usePortfolioStore().portfolio;
</script>
