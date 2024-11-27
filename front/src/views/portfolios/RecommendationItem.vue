<template>
  <v-card class="recommendation-item" outlined>
    <v-card-title>
      {{ productName }}
      <span class="product-type">({{ productType }})</span>
    </v-card-title>
    <v-card-text>
      <p>추천 이유:</p>
      <ul class="reason-list">
        <li>{{ parsedReasons }}</li>
        <li v-for="(reason, index) in parsedReasons" :key="index">
          {{ reason }}
        </li>
      </ul>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from "vue";

// Props
defineProps({
  productName: {
    type: String,
    required: true,
    default: "",
  },
  productType: {
    type: String,
    required: true,
    default: "",
  },
  reasons: {
    type: String,
    required: true,
    default: "",
  },
});

// 추천 이유를 '\n'으로 분리
const parsedReasons = computed(() => {
  return reasons ? reasons.split("\n").filter((reason) => reason.trim() !== "") : [];
});
</script>

<style scoped>
.recommendation-item {
  padding: 16px;
  margin: 16px 0;
}

.product-type {
  font-size: 0.9rem;
  color: #888;
  margin-left: 5px;
}

.reason-list {
  margin-top: 8px;
  padding-left: 16px;
}
</style>
