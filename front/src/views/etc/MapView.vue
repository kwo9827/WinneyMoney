<template>
  <div class="containerbody1">
    <div class="titlepart">
      <h1 class="title">내 근처 은행 찾기</h1>
    </div>
    <!-- <div class="maptitle">내 근처 은행 찾기</div> -->
    <div class="mapcontents">
      <MapInput />
    </div>
  </div>
</template>

<script setup>
import MapInput from '@/components/Map/MapInput.vue';
</script>

<style scoped>
.containerbody1 {
  width: 100%;
  height: 91vh;
  /* background-image: linear-gradient(
      rgba(255, 255, 255, 0.4),
      rgba(255, 255, 255, 0.4)
    ),
    url("@/assets/backgroundimg.png");

  background-size: cover;
  background-repeat: no-repeat; */
  background-color: whitesmoke;
  display: flex;

  flex-direction: column;
  align-items: center;
  margin: 0px 0px;
}

/* .maptitle {
  width: 100%;
  text-align: center;
  margin: 30px 0px;
  font-size: 3rem;
  font-weight: 400;
  font-family: "Noto Sans KR", sans-serif;
  color: rgb(0, 53, 133);
  border-bottom: 1px solid grey;
  padding-bottom: 30px;
} */

.mapcontents {
  display: flex;
  width: 100%;
  height: 60vh;
  justify-content: center;
  align-items: center;
  padding: 20px 20px;
  border-radius: 30px;
}

.titlepart {
  width: 100%;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
  border-bottom: 2px solid lightgray;
}

.title {
  margin-top: 40px;
  font-size: 3rem;
  font-weight: 500;
  font-family: 'Noto Sans KR', sans-serif;
  color: rgb(0, 53, 133);
}
</style>