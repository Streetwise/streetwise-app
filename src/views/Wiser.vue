<template>
  <div class="wiser">
    <ImageVote
      msg="Welche Situation sieht sicherer aus?"
    />
  </div>
</template>

<script>
import ImageVote from '@/components/ImageVote.vue'

export default {
  name: 'wiser',
  components: {
    ImageVote
  }
}
</script>

<style lang="scss">
.wiser {
  text-align: center;
  .lead {
    margin-top: 1em;
  }
}
</style>
