import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueTelegramPlugin } from 'vue-tg'


import App from './App.vue'
import router from './router'

const app = createApp(App)

app.config.devtools = false;


app.use(createPinia())
app.use(router)

app.use(VueTelegramPlugin)

app.mount('#app')

const style = document.createElement('style');
style.innerHTML = `.vue-devtools { display: none !important; }`;
document.head.appendChild(style);

