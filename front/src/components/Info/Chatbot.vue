<template>
  <div class="chatbot-container">
    <!-- 토글 버튼 -->
    <button @click="toggleChatbot" class="toggle-button">
      {{ isChatVisible ? "닫기" : "열기" }} 챗봇
    </button>

    <!-- 채팅창 -->
    <div v-if="isChatVisible" class="chatbot">
      <div class="chat-window">
        <div class="messages">
          <div
            v-for="(msg, index) in chatHistory"
            :key="index"
            :class="msg.role"
          >
            <span>{{ msg.content }}</span>
          </div>
        </div>
        <form @submit.prevent="sendMessage" class="input-form">
          <input
            v-model="userMessage"
            type="text"
            placeholder="메시지를 입력하세요..."
            required
          />
          <button type="submit">전송</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      isChatVisible: false, // 채팅창 표시 여부
      userMessage: "",
      chatHistory: [],
    };
  },
  methods: {
    toggleChatbot() {
      // 채팅창 보이기/숨기기
      this.isChatVisible = !this.isChatVisible;
    },
    async sendMessage() {
      if (!this.userMessage.trim()) return;

      // 사용자 메시지 추가
      this.chatHistory.push({ role: "user", content: this.userMessage });

      try {
        // Django API 호출
        const response = await axios.post("http://127.0.0.1:8000/info/chat/", {
          message: this.userMessage,
        });

        // 챗봇 응답 추가
        this.chatHistory.push({
          role: "assistant",
          content: response.data.reply,
        });
      } catch (error) {
        console.error("API 호출 오류:", error);
        this.chatHistory.push({
          role: "assistant",
          content: "오류가 발생했습니다. 다시 시도해주세요.",
        });
      }

      // 입력 필드 초기화
      this.userMessage = "";
    },
  },
};
</script>

<style scoped>
/* 컨테이너 스타일 */
.chatbot-container {
  position: fixed;
  bottom: 20px;
  left: 20px;
}

/* 토글 버튼 스타일 */
.toggle-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

/* 챗봇 스타일 */
.chatbot {
  width: 300px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.chat-window {
  display: flex;
  flex-direction: column;
  height: 400px;
  overflow: hidden;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.messages .user {
  text-align: right;
  margin-bottom: 5px;
}

.messages .assistant {
  text-align: left;
  margin-bottom: 5px;
}

.input-form {
  display: flex;
  border-top: 1px solid #ccc;
}

.input-form input {
  flex: 1;
  padding: 10px;
  border: none;
  outline: none;
}

.input-form button {
  padding: 10px 20px;
  border: none;
  background: #007bff;
  color: white;
  cursor: pointer;
}
</style>
