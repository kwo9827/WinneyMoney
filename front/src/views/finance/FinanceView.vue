<template>
  <div>
    <RouterLink :to="{name: 'DepositView' }" > 예금 </RouterLink> |
    <RouterLink :to="{name: 'SavingView' }" > 적금 </RouterLink>
  </div>
  <div>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';


</script>

<style scoped>

</style>