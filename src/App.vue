<template>
  <div id="app">
    <AppHeader />
    <router-view/>
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
.vs-popup {
  text-align: left;
}
.fullscreen .vs-popup header { display: none; }
.fullscreen .lightbox-container {
  height: 100%; padding: 10px 0 0; margin: 0px;
  .vs-button-text { color: black; text-shadow: 1px 1px 1px white; }
}
.vs-navbar--header > button.vs-navbar--btn-responsive { visibility: hidden; }
</style>
