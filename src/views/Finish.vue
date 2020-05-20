<template lang="pug">
.finish-page
  h2 Herzlichen Dank f&uuml;r deine Teilnahme!
  p Wir werden das teilen vom Projekt in deine Netzwerke schätzen.
  center.survey-next
    router-link(to="/")
      vs-button(flat='', size='large', color='success', @click='skipSubscribe') Zum Start
  SocialIcons(expand=true)
</template>

<script>
import SocialIcons from '@/components/SocialIcons.vue'

export default {
  name: 'Finish',
  components: {
    SocialIcons
  }
}
</script>

<style lang="scss">
.finish-page {
  h2, p, div {
    margin: 1em 10%;
  }
  .social-icons {
    position: absolute;
    left: 50%;
    margin-top: 1em;
    margin-left: -6em;
    a {
      text-align: left;
      display: block !important;
      width: 12em;
      margin: 1em;
      color: blue;
      font-size: 130%;
    }
  }
}
</style>
