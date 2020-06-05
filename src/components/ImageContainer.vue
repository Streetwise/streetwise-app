<template>
  <img v-bind:src="this.source" v-on:error="this.onImageLoadError">
</template>

<script>
import logError from '@/errorLogger.js'
export default {
  name: 'ImageContainer',
  props: {
    source: '',
    errorHandler: Function
  },
  methods: {
    onImageLoadError () {
      // Set the images as invalid
      this.errorHandler({ message: 'Failed to load image: ' + this.source })
      logError('ImageContainer.vue', 'on image load', 'Failed to load image: ' + this.source)
    }
  }
}
</script>
