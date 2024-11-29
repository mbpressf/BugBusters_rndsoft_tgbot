<template>
  <div id="app">
    <header>
      <h1>User and Message Analytics</h1>
    </header>

    <!-- User Info Section -->
    <section v-if="data.user_info" class="user-info">
      <h2>User Information</h2>
      <ul>
        <li><strong>ID:</strong> {{ data.user_info.id }}</li>
        <li><strong>First Name:</strong> {{ data.user_info.first_name }}</li>
        <li><strong>Username:</strong> {{ data.user_info.username }}</li>
        <li>
          <strong>Active Usernames:</strong>
          <ul>
            <li v-for="username in data.user_info.active_usernames" :key="username">
              {{ username }}
            </li>
          </ul>
        </li>
        <li><strong>Has Private Forwards:</strong> {{ data.user_info.has_private_forwards }}</li>
      </ul>
    </section>

    <!-- Messages Section -->
    <section v-if="data.messages" class="messages">
      <h2>Messages</h2>
      <div v-for="(message, index) in data.messages" :key="index" class="message">
        <h3>Message {{ index + 1 }}</h3>
        <p><strong>Message ID:</strong> {{ message.message.message_id }}</p>
        <p><strong>From:</strong> {{ message.message.from.first_name }} {{ message.message.from.last_name }}</p>
        <p><strong>Text:</strong> {{ message.message.text }}</p>
        <p><strong>Date:</strong> {{ new Date(message.message.date * 1000).toLocaleString() }}</p>
      </div>
    </section>

    <!-- Analytics Section -->
    <section v-if="data.analytics" class="analytics">
      <h2>Analytics</h2>
      <ul>
        <li v-for="(count, command) in data.analytics" :key="command">
          <strong>{{ command }}:</strong> {{ count }}
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
// export default {
//   data() {
//     return {
//       data: {}, // Для хранения JSON данных
//     };
//   },
//   methods: {
//     async fetchData() {
//       try {
//         const response = await fetch("/data.json"); // Загружаем JSON
//         this.data = await response.json(); // Сохраняем в state
//       } catch (error) {
//         console.error("Error fetching data:", error);
//       }
//     },
//   },
//   created() {
//     this.fetchData(); // Загружаем данные при инициализации
//   },
// };


export default {
  data() {
    return {
      data: {}, // Для хранения данных из API
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/data"); // Запрашиваем данные
        this.data = await response.json(); // Сохраняем в state
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
  created() {
    this.fetchData(); // Загружаем данные при инициализации
  },
};


</script>

<style>
  #app{
    font-family: Avenir, Helvetica, Arial, sans-serif;
    margin: 20px;
  }

  header{
    text-align: center;
    margin-bottom: 20px;
  }

  section{
    margin-bottom: 20px;
  }

  h2 {
    color: #2c3e50;
    margin-bottom: 10px;
  }

  ul {
    list-style: none;
    padding: 0;
  }

  li {
    margin: 5px 0;
  }

  .message {
    border: 1px solid #ddd;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
  }

  .analytics ul {
    display: flex;
    flex-wrap: wrap;
  }

  .analytics li {
    margin-right: 10px;
  }
</style>
