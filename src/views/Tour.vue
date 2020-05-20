<template>
  <div>
    <StartTour />
  </div>
</template>

<script>
import VueAwesomeSwiper from 'vue-awesome-swiper'
require('swiper/css/swiper.css')
Vue.use(VueAwesomeSwiper)

import StartTour from '@/components/StartTour.vue'

export default {
  name: 'Tour',
  components: {
    StartTour
  }
}
</script>

<style lang="scss">

</style>
