<template>
  <div class="container1">
    <!-- 특별시/광역시/도 선택 -->
    <select class="select" v-model="selectedProvince">
      <option value="" disabled selected hidden>특별시/광역시/도를 선택하세요</option>
      <option v-for="province in provinces" :key="province" :value="province">
        {{ province }}
      </option>
    </select>

    <!-- 구/군 선택 -->
    <select class="select" v-model="selectedDistrict" :disabled="!selectedProvince">
      <option value="" disabled selected hidden>구/군을 선택하세요</option>
      <option v-for="district in districts" :key="district" :value="district">
        {{ district }}
      </option>
    </select>

    <!-- 동 선택 -->
    <select class="select" v-model="selectedDong" :disabled="!selectedDistrict">
      <option value="" disabled selected hidden>동을 선택하세요</option>
      <option v-for="dong in dongs" :key="dong" :value="dong">
        {{ dong }}
      </option>
    </select>

    <!-- 은행 선택 -->
    <select class="select" v-model="selectedBank">
      <option value="" disabled selected hidden>은행을 선택하세요</option>
      <option v-for="bank in banks" :key="bank">{{ bank }}</option>
    </select>

    <!-- 검색 버튼 -->
    <button class="search-btn" @click="sendMapKeyword">검색!</button>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import Swal from "sweetalert2";

// SweetAlert2 설정
const Toast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  didOpen: (toast) => {
    toast.addEventListener("mouseenter", Swal.stopTimer);
    toast.addEventListener("mouseleave", Swal.resumeTimer);
  },
});

// 데이터
import { useMapStore } from "@/stores/map";
import { defineEmits } from "vue";
const emit = defineEmits(['sendMapKeyword'])
const mapStore = useMapStore();
const koreaData = mapStore.koreaData;

// 상태 관리
const provinces = Object.keys(koreaData);
const selectedProvince = ref("");
const selectedDistrict = ref("");
const selectedDong = ref("");
const selectedBank = ref("");
const districts = ref([]);
const dongs = ref([]);

const banks = [
  "KEB하나은행",
  "SC제일은행",
  "국민은행",
  "신한은행",
  "외환은행",
  "우리은행",
  "한국시티은행",
  "지방은행",
  "경남은행",
  "광주은행",
  "대구은행",
  "부산은행",
  "전북은행",
  "제주은행",
  "기업은행",
  "농협",
  "수협",
  "한국산업은행",
  "한국수출입은행",
];

// `watch`로 선택 변경 감지
watch(selectedProvince, (newProvince) => {
  if (newProvince) {
    console.log(newProvince)
    districts.value = Object.keys(koreaData[newProvince] || {});
    selectedDistrict.value = "";
    selectedDong.value = "";
    dongs.value = [];
  }
});

watch(selectedDistrict, (newDistrict) => {
  if (newDistrict) {
    console.log(newDistrict)
    dongs.value = koreaData[selectedProvince.value]?.[newDistrict] || [];
    selectedDong.value = "";
  }
});

// 키워드 전송
const sendMapKeyword = () => {
  if (!selectedProvince.value || !selectedDistrict.value || !selectedDong.value || !selectedBank.value) {
    Toast.fire({
      icon: "warning",
      title: "모든 항목을 선택해주세요!",
    });
    return;
  }

  const keyword = `${selectedProvince.value} ${selectedDistrict.value} ${selectedDong.value} ${selectedBank.value}`;
  console.log("검색 키워드:", keyword);
  emit("sendMapKeyword", keyword);
};
</script>

<style scoped>
.container1 {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  margin-right: 50px;
}

.select {
  margin: 10px;
  padding: 8px;
  border: 1px solid #4db7e5;
  border-radius: 5px;
  background-color: white;
  color: #1c5f82;
}

.search-btn {
  margin-top: 10px;
  border: none;
  border-radius: 30px; /* 버튼 모서리 둥글게 */
  background: linear-gradient(90deg, #007aff, #00d4ff); /* 그라데이션 */
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  padding: 10px 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease; /* 부드러운 전환 효과 */
}

.search-btn:hover {
  background: linear-gradient(90deg, #0056b3, #009ad4); /* 호버 시 색상 변경 */
  transform: scale(1.05); /* 살짝 커짐 효과 */
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 강조 */
}

.search-btn:active {
  transform: scale(0.95); /* 클릭 시 눌리는 효과 */
}

.search-btn svg {
  margin-right: 8px; /* 아이콘과 텍스트 간격 */
  width: 20px;
  height: 20px;
}
</style>
