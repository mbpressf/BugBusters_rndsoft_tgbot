<template>
  <div>
    <!-- Поля для фильтрации -->
    <div class="filters">
      <input 
        type="text" 
        v-model="searchUsername" 
        placeholder="Введите имя пользователя"
        class="input-field"
      />
      <select v-model="selectedChat" class="select-field">
        <option v-for="(chat, chatId) in data" :key="chatId" :value="chatId">
          {{ chat.name }}
        </option>
      </select>
      <button @click="showModal = true" class="stats-button">Показать статистику</button>
    </div>

    <!-- Список сообщений -->
    <div v-if="filteredMessages.length > 0" class="messages">
      <h2 class="chat-title">
        {{ data[selectedChat]?.name || 'Выберите чат' }}
      </h2>
      <div 
        class="message" 
        v-for="(message, index) in filteredMessages" 
        :key="index"
      >
        <div class="message-meta">
          <span class="message-time">{{ message.time }}</span>
          <span class="message-username">{{ message.username || 'Аноним' }}</span>
        </div>
        <div class="message-text">
          {{ message.text_message || 'Сообщение без текста' }}
        </div>
      </div>
    </div>

    <!-- Если ничего не найдено -->
    <div v-else-if="data" class="no-messages">
      <p>Сообщения не найдены.</p>
    </div>

    <!-- Загрузка -->
    <div v-if="!data" class="loading">
      <p>Загрузка данных...</p>
    </div>

    <!-- Модальное окно -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h2>Статистика</h2>
        <p v-if="searchUsername">
          Сообщения пользователя <strong>{{ searchUsername }}</strong>: {{ filteredMessages.length }} из {{ totalMessages }}.
        </p>
        <p v-else>
          Общее количество сообщений в чате: {{ totalMessages }}.
        </p>

        <!-- Диаграмма -->
        <div class="chart-container">
          <PieChart
            :labels="chartLabels"
            :data="chartData"
            :colors="chartColors"
          />
        </div>

        <button @click="showModal = false" class="close-button">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import PieChart from './components/PieChart.vue'; // Компонент диаграммы

export default {
  components: {
    PieChart,
  },
  data() {
    return {
      data: null, // Данные чатов
      selectedChat: null, // Выбранный чат
      searchUsername: '', // Имя пользователя для поиска
      showModal: false, // Показывать ли модальное окно
    };
  },
  computed: {
    filteredMessages() {
      if (!this.selectedChat || !this.data) return [];
      
      const chat = this.data[this.selectedChat];
      if (!chat) return [];

      return chat.messages.filter(message =>
        (!this.searchUsername || (message.username || '').toLowerCase().includes(this.searchUsername.toLowerCase()))
      );
    },
    totalMessages() {
      if (!this.selectedChat || !this.data) return 0;

      const chat = this.data[this.selectedChat];
      return chat.messages.length;
    },
    // Расчет статистики по каждому пользователю в чате
    userStats() {
      if (!this.selectedChat || !this.data) return {};

      const chat = this.data[this.selectedChat];
      const userMessages = {};

      chat.messages.forEach(message => {
        const username = message.username || 'Аноним';
        if (!userMessages[username]) {
          userMessages[username] = 0;
        }
        userMessages[username]++;
      });

      return userMessages;
    },
    chartLabels() {
      const userMessages = this.userStats;
      return Object.keys(userMessages);
    },
    chartData() {
      const userMessages = this.userStats;
      const total = this.totalMessages;
      return Object.values(userMessages).map(count => (count / total) * 100);
    },
    chartColors() {
      // Генерация случайных цветов для пользователей
      const colors = [];
      const numUsers = this.chartLabels.length;
      for (let i = 0; i < numUsers; i++) {
        colors.push(`hsl(${(i * 360) / numUsers}, 100%, 50%)`);
      }
      return colors;
    },
  },
  mounted() {
    axios.get('http://localhost:5000/api/data')
      .then(response => {
        this.data = response.data;
        // Устанавливаем первый чат как выбранный по умолчанию
        this.selectedChat = Object.keys(this.data)[0];
      })
      .catch(error => {
        console.error("Ошибка при загрузке данных:", error);
      });
  },
};
</script>

<style scoped>
/* Стили для полей фильтрации */
.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.input-field, .select-field, .stats-button {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.stats-button {
  background-color: #4CAF50;
  color: #fff;
  cursor: pointer;
}

.stats-button:hover {
  background-color: #45a049;
}

/* Сообщения */
.messages {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-field{
  border-radius: 30px;
  background-color: #333;
  border: 2px #333 solid;
  color: #ddd;
}

.select-field{
  border-radius: 30px;
  background-color: #333;
  border: 2px #333 solid;
  color: #ddd;
}

.stats-button{
  border-radius: 30px;
  border: px #333 solid;
  color: #ddd;
}

.message {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.message-username{
  font-weight: 600;
  color: #333;
}

.message-meta {
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
}

.message-text {
  font-size: 14px;
  color: #333;
  word-wrap: break-word;
}

/* Модальное окно */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-overlay p, h2{
  color: rgb(61, 61, 61);
  font-weight: 700;
}

.modal {
  background: #fff;
  padding: 20px 20px 80px 20px;
  border-radius: 10px;
  width: 400px;
  text-align: center;
}

.close-button {
  background-color: #f44336;
  position: relative;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  bottom: -100px;
}

.close-button:hover {
  background-color: #d32f2f;
}

.chart-container {
  margin: 20px 0;
  height: 200px;
}

/* Если сообщения не найдены */
.no-messages {
  text-align: center;
  color: #999;
  font-size: 16px;
}
</style>
