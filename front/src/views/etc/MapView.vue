<template>
  <div class="container">
    <div class="map-container">
      <MapInput />
    </div>
  </div>
</template>

<script setup>
import MapInput from '@/components/Map/MapInput.vue';
</script>

<style scoped>
.container {
  width: 100%;
  height: 100vh; /* 화면 전체를 채움 */
  margin: 0;
  padding: 0;
}

.map-container {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>
