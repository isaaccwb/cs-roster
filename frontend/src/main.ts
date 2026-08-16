import './styles/reset.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, DatasetComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

use([
  CanvasRenderer, BarChart, LineChart, PieChart,
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, DatasetComponent
])

const app = createApp(App)

app.component('v-chart', VChart)
app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
