<template>
  <div id="app">
    <vs-navbar
        color="secondary"
        text-color="rgba(255,255,255,1)"
        class="navbar"
    >
      <vs-navbar-title>
        Streetwise
      </vs-navbar-title>

      <vs-navbar-item>
        <router-link to="/">Start</router-link>
      </vs-navbar-item><vs-navbar-item>
        <router-link to="/tour">Tour</router-link>
      </vs-navbar-item><vs-navbar-item>
        <router-link to="/wise">Umfrage</router-link>
      </vs-navbar-item><vs-navbar-item>
        <a href="/api">API</a>
      </vs-navbar-item>
    </vs-navbar>

    <router-view/>

    <div id="logos"><img src="@/assets/logo.png"></div>
  </div>
</template>

<style lang="scss">
#app {
  font-family: 'OpenSans', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #5b5777;
}
#logos {
  position: absolute; bottom: 0; right: 0; border: 0;
  img { width: 90px; }
}

.vs-navbar--title {
  float: left;
  font-size: 120%;
}

.vs-navbar--item a {
  text-decoration: none;
  font-weight: bold;
  color: #fff;
}
</style>
