<template>
  <div class="header">
    <vs-navbar
        color="secondary"
        text-color="rgba(255,255,255,1)"
        class="navbar"
    >

      <div slot="title">
        <vs-navbar-title>
          Streetwise
        </vs-navbar-title>
      </div>

      <vs-navbar-item>
        <router-link to="/">Start</router-link>
      </vs-navbar-item><vs-navbar-item>
        <router-link to="/wise">Umfrage</router-link>
      </vs-navbar-item><vs-navbar-item>
        <router-link to="/complete">Formular</router-link>
      </vs-navbar-item><vs-navbar-item>
        <router-link to="/tour">Mockup</router-link>
      </vs-navbar-item><vs-navbar-item>
        <a href="/api">API</a>
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
.vs-navbar--title {
  font-size: 120%;
}
.vs-navbar--item {
  opacity: 0.5;
}
</style>
