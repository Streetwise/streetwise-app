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
#app, .vs-popup, .vs-dialog {
  font-family: 'OpenSans', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  overflow-x: hidden;
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

// Note: for compatibility with IE11 - configured in main.js
.vuesax-app-is-ltr {
  .vs-button-primary { background-color: rgb(91, 60, 196) }
  .vs-button-success { background-color: rgb(23, 201, 100) }
  .vs-button-danger { background-color:  rgb(242, 19, 93) }
  .vs-button-warning { background-color: rgb(255, 130, 0) }
  .vs-button-light { background-color:   rgb(200, 200, 200); color: black; }
  .vs-button-dark { background-color:    rgb(36, 33, 69) }
}
#app .vs-button-light { color: black; }
.together { white-space: nowrap; }

</style>
