import Vue from 'vue'
import Router from 'vue-router'

import Start from './views/Start.vue'
import Wiser from './views/Wiser.vue'
import Complete from './views/Complete.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'start',
      component: Start
    },
    {
      path: '/finish',
      name: 'finish',
      component: Start
    },
    {
      path: '/wise',
      name: 'wise',
      component: Wiser,
      props: true
    },
    {
      path: '/complete/:responses',
      name: 'complete',
      component: Complete,
      props: true
    }
  ]
})
