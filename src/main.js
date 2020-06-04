import Vue from 'vue'
import Vuesax from 'vuesax'

import App from './App.vue'

import router from './router'
import store from './store'

import 'vuesax/dist/vuesax.css'
import 'material-icons/iconfont/material-icons.css'

import './filters'

Vue.use(Vuesax, {
  // Note: see also CSS specified in App.vue
  colors: {
    primary: 'rgb(91, 60, 196)',
    success: 'rgb(23, 201, 100)',
    danger: 'rgb(242, 19, 93)',
    warning: 'rgb(255, 130, 0)',
    light: 'rgb(200, 200, 200)',
    dark: 'rgb(36, 33, 69)'
  }
})

Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  // console.log(to)
  // Implement Navigation Guards
  if (from.name === 'wise' && to.name === 'start' && to.fullPath === '/?reason=net_err') {
    // Do not prompt for confirmation while going to /start on network error
    next()
  } else if (from.name === 'wise' && to.name !== 'complete' && to.name !== 'finish') {
    return next(window.confirm('Bist du dir sicher, dass du die Umfrage verlassen willst?'))
  }
  next()
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
