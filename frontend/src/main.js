import { createApp } from 'vue'
import App from '@/App.vue'
import components from '@/components/UI';
import router from '@/router'
import store from '@/store'

import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const toastOptions = {
    transition: "Vue-Toastification__slideBlurred",
    maxToasts: 5,
    newestOnTop: false,
    position: "top-right",
    timeout: 5000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.4,
    showCloseButtonOnHover: true,
    hideProgressBar: false,
    closeButton: "button",
    icon: true,
    rtl: false
};

const app = createApp(App)

components.forEach(component => {
    app.component(component.name, component)
})

app
    .use(store)
    .use(router)
    .use(Toast, toastOptions)
    .mount('#app')
