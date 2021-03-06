import Vue from 'vue'
import Router from 'vue-router'
import Meta from 'vue-meta'

import Start from './views/Start.vue'
import Wiser from './views/Wiser.vue'
import Voting from './views/Voting.vue'
import Complete from './views/Complete.vue'
import Finish from './views/Finish.vue'

Vue.use(Router)
Vue.use(Meta)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'start',
      component: Start,
      props: true
    },
    {
      path: '/wise',
      name: 'wise',
      component: Wiser,
      props: true
    },
    {
      path: '/vote',
      name: 'vote',
      component: Voting,
      props: true
    },
    {
      path: '/complete/:responses',
      name: 'complete',
      component: Complete,
      props: true
    },
    {
      path: '/finish',
      name: 'finish',
      component: Finish,
      props: true
    }
  ]
})
