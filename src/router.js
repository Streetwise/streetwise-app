import Vue from 'vue'
import Router from 'vue-router'

import Start from './views/Start.vue'
import Wiser from './views/Wiser.vue'
import Complete from './views/Complete.vue'
import Tour from './views/Tour.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'start',
      component: Start
    },
    {
      path: '/wise',
      name: 'wise',
      component: Wiser
    },
    {
      path: '/complete',
      name: 'complete',
      component: Complete
    },
    {
      path: '/tour',
      name: 'tour',
      component: Tour
    }
  ]
})
