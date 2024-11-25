<template>
  <div class="map-container">
    <!-- 검색 및 드롭다운 -->
    <!-- <div class="search-bar">
      <input
        type="text"
        class="search-input"
        placeholder="은행 이름이나 주소를 검색하세요"
        v-model="searchKeyword"
        @keypress.enter="searchByKeyword"
      />
      <button class="search-button" @click="searchByKeyword">검색</button>
    </div> -->
    <div class="dropdowns">
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
      <button class="search-button" @click="searchByDropdown">검색</button>
    </div>
    <!-- 지도 -->
    <div id="map"></div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
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

// 지도 상태 관리
let map, ps, infowindow;

// 데이터
import { useMapStore } from "@/stores/map";
const mapStore = useMapStore();
const koreaData = mapStore.koreaData;

// 상태 관리
const searchKeyword = ref("");
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

// 지도 초기화
onMounted(() => {
  const mapContainer = document.getElementById("map");
  const mapOption = {
    center: new kakao.maps.LatLng(37.566826, 126.9786567), // 초기 중심 좌표 (서울)
    level: 8, // 초기 확대 레벨
  };
  map = new kakao.maps.Map(mapContainer, mapOption); // 지도 생성
  ps = new kakao.maps.services.Places(); // 장소 검색 객체 생성
  infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
});

// `watch`로 선택 변경 감지
watch(selectedProvince, (newProvince) => {
  if (newProvince) {
    districts.value = Object.keys(koreaData[newProvince] || {});
    selectedDistrict.value = "";
    selectedDong.value = "";
    dongs.value = [];
  }
});

watch(selectedDistrict, (newDistrict) => {
  if (newDistrict) {
    dongs.value = koreaData[selectedProvince.value]?.[newDistrict] || [];
    selectedDong.value = "";
  }
});

// 키워드로 검색
const searchByKeyword = () => {
  if (!searchKeyword.value.trim()) {
    Toast.fire({
      icon: "warning",
      title: "검색 키워드를 입력해주세요!",
    });
    return;
  }
  ps.keywordSearch(searchKeyword.value, placesSearchCB);
};

// 드롭다운 선택으로 검색
const searchByDropdown = () => {
  if (!selectedProvince.value || !selectedDistrict.value || !selectedDong.value || !selectedBank.value) {
    Toast.fire({
      icon: "warning",
      title: "모든 항목을 선택해주세요!",
    });
    return;
  }
  const keyword = `${selectedProvince.value} ${selectedDistrict.value} ${selectedDong.value} ${selectedBank.value}`;
  ps.keywordSearch(keyword, placesSearchCB);
};

// 장소 검색 콜백
const placesSearchCB = (data, status, pagination) => {
  if (status === kakao.maps.services.Status.OK) {
    // 검색된 장소가 있으면 지도에 표시
    const bounds = new kakao.maps.LatLngBounds();
    data.forEach((place) => {
      displayMarker(place);
      bounds.extend(new kakao.maps.LatLng(place.y, place.x));
    });
    map.setBounds(bounds); // 검색된 장소로 지도 범위 조정
  } else {
    Toast.fire({
      icon: "error",
      title: "검색 결과가 없습니다!",
    });
  }
};

// 마커 표시
const displayMarker = (place) => {
  const marker = new kakao.maps.Marker({
    map,
    position: new kakao.maps.LatLng(place.y, place.x),
  });
  kakao.maps.event.addListener(marker, "click", () => {
    infowindow.setContent(`<div style="padding:5px;font-size:12px;">${place.place_name}</div>`);
    infowindow.open(map, marker);
  });
};
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
  position: relative;
}

.search-bar {
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  gap: 10px;
  z-index: 10;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.search-input {
  width: 300px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.search-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.search-button:hover {
  background-color: #2980b9;
}

.dropdowns {
  position: absolute;
  top: 80px;
  left: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 10;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  background-color: #ffffff;
}

#map {
  width: 100%;
  height: 100%;
}
</style>
