import Vue from 'vue'
import Router from 'vue-router'

import Home from './views/Home.vue'
import Wiser from './views/Wiser.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/wise',
      name: 'wise',
      component: Wiser
    }
  ]
})
