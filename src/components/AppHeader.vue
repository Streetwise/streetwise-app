<template>
  <div class="header">
    <vs-navbar
        color="secondary"
        text-color="rgba(255,255,255,1)"
        class="navbar"
    >

      <div slot="title">
        <vs-navbar-title>
          <router-link to="/">
            <img class="logo" src="@/assets/streetwise_Logo.png" alt="streetwise app" title="Zum Start">
          </router-link>
        </vs-navbar-title>
      </div>
      <!--
      <vs-navbar-item v-show="false">
        <a href="https://forms.gle/fDcXHYkSire7GRiU9" target="_blank">Feedback</a>
      </vs-navbar-item>
      <vs-navbar-item v-show="false">
        <a href="https://streetwise.space/start" target="_blank">Hilfe</a>
      </vs-navbar-item> -->
    </vs-navbar>
  </div>
</template>

<script>
export default {
  name: 'AppHeader',
  props: {
  }
}
</script>

<style scoped lang="scss">
.devpanel { display: none !important }
.vs-navbar--title {
  font-size: 120%;
  padding-top: 4px;
  font-size: 0px;
  color: transparent;
  img {
    height: 30px;
  }
  a {
    color: black;
    u {
      border-bottom: 2px solid blue;
    }
  }
}
header { min-height: 2em; }
@media screen and (max-height: 400px) {
  .vs-navbar--title { margin: 0px; padding-top: 0px; top: 5px; right: 0px; position: absolute }
}
@media screen and (min-height: 800px) {
  header { min-height: 3em; }
  .vs-navbar--title { margin-top: 0px; }
}
</style>
