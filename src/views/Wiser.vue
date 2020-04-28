<template>
  <div class="wiser">
    <h4 class="lead">Wählen Sie das Bild, das sich sicherer anfühlt.</h4>

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
