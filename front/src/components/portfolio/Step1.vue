<template>
  <div>
    <label for="name">포트폴리오 이름:</label>
    <input id="name" v-model="portfolio.name" type="text" />
    <button @click="$emit('next')">다음</button>
  </div>
</template>

<script setup>
import { usePortfolioStore } from "@/stores/portfolio";

const portfolio = usePortfolioStore().portfolio;
</script>
