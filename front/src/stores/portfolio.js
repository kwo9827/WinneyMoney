import { defineStore } from "pinia";
import axios from "axios";
import { reactive } from "vue";
import { useAccountStore } from "@/stores/accounts";

export const usePortfolioStore = defineStore("portfolio", () => {
  // Portfolio 상태를 reactive로 관리
  const portfolio = reactive({
    name: "",
    predictedEconomy: null,
    riskPreference: null,
    totalInvestment: 0,
    stocks: [],
    cryptocurrencies: [],
  });

  let portfolioId = null; // 포트폴리오 ID 저장
  let recommendations = reactive([]); // 추천 상품 저장

  // 포트폴리오 생성
  const createPortfolio = async () => {
    const accountStore = useAccountStore();
    const token = accountStore.token;

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/portfolios/",
        portfolio,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );
      portfolioId = response.data.id;
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data || error.message);
    }
  };

  // 주식 추가
  const addStock = async (stock) => {
    const accountStore = useAccountStore();
    const token = accountStore.token;

    if (!portfolioId) {
      throw new Error("포트폴리오가 생성되지 않았습니다.");
    }

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/portfolios/${portfolioId}/stocks/`,
        stock,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      portfolio.stocks.push(response.data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data || error.message);
    }
  };

// 주식 수정
const updateStock = async (updatedStock) => {
  const accountStore = useAccountStore();
  const token = accountStore.token;

  if (!portfolioId) {
    throw new Error("포트폴리오가 생성되지 않았습니다.");
  }

  try {
    const response = await axios.put(
      `http://127.0.0.1:8000/portfolios/${portfolioId}/stocks/${updatedStock.id}/`,
      updatedStock,
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    // portfolio.stocks 내부의 added_stocks에서 수정
      portfolio.stocks.forEach((group) => {
        console.log('그룹',group)
        const index = group.added_stocks.findIndex(
        (stock) => stock.id === updatedStock.id
      );

      if (index !== -1) {
        group.added_stocks[index] = response.data; // 수정된 데이터 반영
        console.log("수정된 데이터:", portfolio.stocks);
      }
    });

      return response.data;
    } catch (error) {
      throw new Error(error.response?.data || error.message);
    }
  };
  
  // 주식 삭제
  const deleteStock = async (stockId) => {
    const accountStore = useAccountStore();
    const token = accountStore.token;

    if (!portfolioId) {
      throw new Error("포트폴리오가 생성되지 않았습니다.");
    }

    try {
      await axios.delete(
        `http://127.0.0.1:8000/portfolios/${portfolioId}/stocks/${stockId}/delete/`,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      // portfolio.stocks 내부의 데이터 삭제
      portfolio.stocks.forEach((group) => {
        const index = group.added_stocks.findIndex(
          (stock) => stock.id === stockId
        );

        if (index !== -1) {
          group.added_stocks.splice(index, 1); // 데이터 삭제
          console.log("삭제된 후 주식 데이터:", portfolio.stocks);
        }
      });

      return true;
    } catch (error) {
      throw new Error(error.response?.data || error.message);
    }
  };


  // 암호화폐 추가
  const addCrypto = async (payload) => {
    const accountStore = useAccountStore();
    const token = accountStore.token;

    if (!portfolioId) {
      throw new Error("포트폴리오가 생성되지 않았습니다.");
    }

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/portfolios/${portfolioId}/crypto/`,
        payload,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      portfolio.cryptocurrencies.push(response.data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data || error.message);
    }
  };

  // 암호화폐 수정
  const updateCrypto = async (updatedCrypto) => {
    const accountStore = useAccountStore();
    const token = accountStore.token;

    if (!portfolioId) {
      throw new Error("포트폴리오가 생성되지 않았습니다.");
    }

    try {
      const response = await axios.put(
        `http://127.0.0.1:8000/portfolios/${portfolioId}/crypto/${updatedCrypto.id}/`,
        updatedCrypto,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      // portfolio.cryptocurrencies 내부의 데이터 수정
      portfolio.cryptocurrencies.forEach((group) => {
        console.log('그룹',group)
        const index = group.added_cryptos.findIndex(
          (crypto) => crypto.id === updatedCrypto.id
        );

        if (index !== -1) {
          group.added_cryptos[index] = response.data; // 수정된 데이터 반영
          console.log("수정된 암호화폐 데이터:", portfolio.cryptocurrencies);
        }
      });

      return response.data;
    } catch (error) {
      throw new Error(error.response?.data || error.message);
    }
  };

  // 암호화폐 삭제
  const deleteCrypto = async (cryptoId) => {
    const accountStore = useAccountStore();
    const token = accountStore.token;
    console.log(cryptoId)
    if (!portfolioId) {
      throw new Error("포트폴리오가 생성되지 않았습니다.");
    }

    try {
      await axios.delete(
        `http://127.0.0.1:8000/portfolios/${portfolioId}/crypto/${cryptoId}/delete/`,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );
      console.log(cryptoId)
      // portfolio.cryptocurrencies 내부의 데이터 삭제
      portfolio.cryptocurrencies.forEach((group) => {
        console.log('그룹',group)
        const index = group.added_cryptos.findIndex(
          (crypto) => crypto.id === cryptoId
        );

        if (index !== -1) {
          group.added_cryptos.splice(index, 1); // 데이터 삭제
          console.log("삭제된 후 암호화폐 데이터:", portfolio.cryptocurrencies);
        }
      });

      return true;
    } catch (error) {
      throw new Error(error.response?.data || error.message);
    }
  };


  // 추천 상품 조회
  const fetchRecommendations = async () => {
    const accountStore = useAccountStore();
    const token = accountStore.token;

    if (!portfolioId) {
      throw new Error("포트폴리오가 생성되지 않았습니다.");
    }

    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/portfolios/${portfolioId}/recommend/`,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );
      recommendations.splice(0, recommendations.length, ...response.data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data || error.message);
    }
  };

  // 포트폴리오 초기화
  const resetPortfolio = () => {
    Object.assign(portfolio, {
      name: "",
      predictedEconomy: null,
      riskPreference: null,
      totalInvestment: 0,
      stocks: [],
      cryptocurrencies: [],
    });
    portfolioId = null;
    recommendations.splice(0);
  };

  return {
    portfolio,
    portfolioId,
    recommendations,
    createPortfolio,
    addStock,
    updateStock,
    deleteStock,
    addCrypto,
    updateCrypto,
    deleteCrypto,
    fetchRecommendations,
    resetPortfolio,
  };
});
