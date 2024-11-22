import { defineStore } from "pinia";
import axios from "axios";

export const usePortfolioStore = defineStore("portfolio", {
  state: () => ({
    portfolio: {
      name: "",
      predictedEconomy: null,
      riskPreference: null,
      totalInvestment: 0,
      stocks: [],
      bonds: [],
    },
  }),
  actions: {
    // 포트폴리오 생성 요청
    async createPortfolio() {
      try {
        const response = await axios.post("/api/portfolio/create/", this.portfolio);
        console.log("생성 완료:", response.data);
        return response.data;
      } catch (error) {
        throw new Error(error.response?.data || error.message);
      }
    },
  },
});
