<template>
  <div class="header">
    <vs-navbar
        color="secondary"
        text-color="rgba(255,255,255,1)"
        class="navbar"
    >

      <div slot="title">
        <vs-navbar-title>
          <router-link to="/">street<u>wise</u> app</router-link>
        </vs-navbar-title>
      </div>
      <vs-navbar-item>
        <a href="mailto:support@streetwise.space">Hilfe</a>
      </vs-navbar-item>
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
.devpanel { display: none }
.vs-navbar--title {
  font-size: 120%;
  a {
    color: black;
    u {
      border-bottom: 2px solid blue;
    }
  }
}
</style>
