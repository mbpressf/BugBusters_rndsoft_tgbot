<template>
  <div>
    <!-- Информация о пользователе -->
    <div class="user-info" v-if="data">
      <p><strong>ID:</strong> {{ data.user_info.id }}</p>
      <p><strong>Имя:</strong> {{ data.user_info.first_name }}</p>
      <p><strong>Пользователь:</strong> {{ data.user_info.username }}</p>
    </div>

    <!-- Сообщения -->
    <div class="messages" v-if="data">
      <div 
        class="message" 
        v-for="(message, index) in data.messages" 
        :key="index"
      >
        <div class="message-meta">
          <span class="message-time">{{ message.date }} {{ message.time }}</span>
        </div>
        <div 
          class="message-text" 
          :class="{ 'no-text': !message.text }"
        >
          {{ message.text || 'Сообщение без текста' }}
        </div>
      </div>
    </div>
    <div v-else class="loading">
      <p>Загрузка данных...щащаща</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      data: null,
    };
  },
  mounted() {
    axios.get('http://localhost:5000/api/data')
      .then(response => {
        this.data = response.data;
      })
      .catch(error => {
        console.error("Ошибка при загрузке данных:", error);
      });
  },
};
</script>

<style scoped>
.vue-devtools {
  display: none !important;
}
/* Информация о пользователе */
.user-info {
  margin-bottom: 20px;
  font-family: Arial, sans-serif;
  font-size: 14px;
  color: #333;
}

.user-info p {
  margin: 5px 0;
  font-size: 20px;
  color: #ddd;
}

/* Сообщения */
.messages {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Отдельное сообщение */
.message {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Время сообщения */
.message-meta {
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
}

/* Текст сообщения */
.message-text {
  font-size: 14px;
  color: #161616;
  word-wrap: break-word;
  font-weight: 600;
}

/* Стили для пустых сообщений */
.message-text.no-text {
  font-style: italic;
  color: #bbb;
}

/* Индикатор загрузки */
.loading {
  text-align: center;
  color: #999;
  font-size: 16px;
}
</style>
