import Vue from 'vue'
import Router from 'vue-router'

import Start from './views/Start.vue'
import Tour from './views/Tour.vue'
import Wiser from './views/Wiser.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'start',
      component: Start
    },
    {
      path: '/tour',
      name: 'tour',
      component: Tour
    },
    {
      path: '/wise',
      name: 'wise',
      component: Wiser
    }
  ]
})
