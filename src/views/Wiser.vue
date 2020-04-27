<template>
  <div class="wiser">
    <p class="lead">Choose the image that feels safer.</p>

    <ImageVote />
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
}
</style>
