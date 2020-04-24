<template>
  <div id="app">
    <div id="logos"><img src="@/assets/logo.png"></div>

    <router-view/>

    <div id="nav">
      <router-link to="/">Tour</router-link> |
      <router-link to="/wise">Evaluation</router-link> |
      <a href="/api">API</a>
    </div>
  </div>
</template>

<style lang="scss">
#logos {
  position: absolute; top: 0; right: 0; border: 0;
  img { width: 90px; }
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
#plus {
  padding: 0 20px 0 20px;
  display: inline-block;
  font-size: 50px;
  vertical-align: top;
  line-height: 100px;
}

</style>
