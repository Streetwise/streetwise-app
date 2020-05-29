<template>
  <img v-bind:src="this.source" v-on:error="this.onImageLoadError">
</template>

<script>
import logError from '@/errorLogger.js'
export default {
  name: 'ImageContainer',
  props: {
    source: ''
  },
  methods: {
    onImageLoadError () {
      // Set the images as invalid
      logError('ImageContainer.vue', 'on image load', 'Failed to load image: ' + this.source)
      this.$store.commit('invalidImages')
    }
  }
}
</script>
