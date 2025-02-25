import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import {
    create,
    NCard, NModal, NInput, NButton, NTabs, NTabPane, NSelect, NFormItem, NForm, NIcon, NInputNumber, NSpace, NText, NTooltip, NSpin, NResult
} from 'naive-ui'

const naive = create({
    components: [NCard, NModal, NInput, NButton, NTabs, NTabPane, NSelect, NFormItem, NForm, NIcon, NInputNumber, NSpace, NText, NTooltip, NSpin, NResult]
})
createApp(App).use(router).use(naive).mount('#app')
