<template>
  <div id="app">
    <AppHeader />
    <router-view/>
    <div id="logos"><img src="@/assets/streetwise_Logo.png"></div>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'

export default {
  name: 'App',
  components: {
    AppHeader
  }
}
</script>

<style lang="scss">
#app, .vs-popup {
  font-family: 'OpenSans', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #5b5777;
}
@media screen and (max-width: 600px) {
  html { overflow: hidden; }
}
.vs-popup {
  text-align: left;
}
.lightbox-container {
  height: 100%;
}
#logos {
  display: none;
  position: absolute; z-index: -99;
  bottom: 0; right: 0; border: 0;
  img { width: 90px; }
}
</style>
