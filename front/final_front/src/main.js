
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import vueDebounce from 'vue-debounce'
const app = createApp(App)
const pinia = createPinia()
app.use(createPinia())
app.use(router)
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
app.directive('debounce', vueDebounce({ lock: true }))
app.mount('#app')
pinia.use(piniaPluginPersistedstate)
