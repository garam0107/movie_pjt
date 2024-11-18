
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()
app.use(createPinia())
app.use(router)
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
app.mount('#app')
pinia.use(piniaPluginPersistedstate)
