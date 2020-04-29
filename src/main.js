import Vue from 'vue'
import Vuesax from 'vuesax'
import VueAwesomeSwiper from 'vue-awesome-swiper'

import App from './App.vue'

import router from './router'
import store from './store'

import 'vuesax/dist/vuesax.css'
import 'material-icons/iconfont/material-icons.css'

import './filters'

Vue.use(Vuesax, {
  colors: {
    primary: '#5b3cc4',
    success: 'rgb(23, 201, 100)',
    danger: 'rgb(242, 19, 93)',
    warning: 'rgb(255, 130, 0)',
    dark: 'rgb(36, 33, 69)'
  }
})

require('swiper/css/swiper.css')
Vue.use(VueAwesomeSwiper)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
