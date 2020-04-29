<template>
  <div class="header">
    <vs-navbar
        color="secondary"
        text-color="rgba(255,255,255,1)"
        class="navbar"
    >

      <div slot="title">
        <vs-navbar-title>
          <router-link to="/">Street<u>wise</u></router-link>
        </vs-navbar-title>
      </div>

      <vs-navbar-item>
        <router-link to="/">Home</router-link>
      </vs-navbar-item><vs-navbar-item>
        <router-link to="/wise">Umfrage</router-link>
      </vs-navbar-item><vs-navbar-item>
        <router-link to="/complete">Formular</router-link>
      </vs-navbar-item><vs-navbar-item>
        <router-link to="/tour">Mockup</router-link>
      </vs-navbar-item><vs-navbar-item>
        <a href="/api">API</a>
      </vs-navbar-item><vs-navbar-item>
        <a href="mailto:support@streetwise.space">Kontakt</a>
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
  a {
    color: black;
    u {
      border-bottom: 2px solid blue;
    }
  }
}
.vs-navbar--item {
  opacity: 0.5;
}
</style>
