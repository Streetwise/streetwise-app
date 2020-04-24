<template>
  <swiper ref="mySwiper" :options="swiperOptions">
    <swiper-slide>
      <img src="@/assets/mockup/1.png">
    </swiper-slide><swiper-slide>
      <img src="@/assets/mockup/2.png">
    </swiper-slide><swiper-slide>
      <img src="@/assets/mockup/3.png">
    </swiper-slide><swiper-slide>
      <img src="@/assets/mockup/4.png">
    </swiper-slide><swiper-slide>
      <img src="@/assets/mockup/5.png">
    </swiper-slide>
    <div class="swiper-pagination" slot="pagination"></div>
  </swiper>
</template>

<script>

export default {
  name: 'carrousel',
  data () {
    return {
      swiperOptions: {
        pagination: {
          el: '.swiper-pagination'
        }
        // Some Swiper option/callback...
      }
    }
  },
  computed: {
    swiper () {
      return this.$refs.mySwiper.$swiper
    }
  },
  mounted () {
    console.log('Current Swiper instance object', this.swiper)
    this.swiper.slideTo(3, 1000, false)
  }
}
</script>

<style scoped lang="scss">
img {
  width: 80%;
  max-width: 700px;
}
</style>
