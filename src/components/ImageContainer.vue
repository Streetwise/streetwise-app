<template>
  <img v-bind:src="this.source" v-on:error="this.onImageLoadError">
</template>

<script>
export default {
  name: 'ImageContainer',
  props: {
    source: ''
  },
  methods: {
    onImageLoadError () {
      // Set the images as invalid
      this.$store.commit('invalidImages')
    }
  },
  created: function () {
    console.log('created Image container', this.leftImageSrc)
  },
  updated: function () {
    console.log('updated Image container', this.leftImageSrc)
  }
}
</script>
