<template>
  <div class="title">
    <vs-navbar-title>
      <router-link to="/">
        <img class="logo" src="@/assets/streetwise_Logo.png" alt="streetwise app" title="Zum Start">
      </router-link>
    </vs-navbar-title>
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
.title {
  display: flex;
  flex-direction: row;
  padding: 0.5em;
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
</style>
