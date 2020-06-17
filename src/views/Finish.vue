<template lang="pug">
.finish-page
  h2 Herzlichen Dank f&uuml;r deine Teilnahme.
  p Teile die streetwise Umfrage mit deinen Freunden und Bekannten!
  center
    ProgressGoals
  SocialIcons(expand=true)
  .footer
    router-link(to="/")
      vs-button(flat, size='large', color='dark') schliessen
    router-link(:to="{ name: 'wise', params: { didsurvey: true, didfeedback: true }}")
      vs-button(flat, size='large', color='success') weitere Bilder bewerten
</template>

<script>
import SocialIcons from '@/components/SocialIcons.vue'
import ProgressGoals from '@/components/ProgressGoals.vue'

export default {
  name: 'Finish',
  components: {
    SocialIcons,
    ProgressGoals
  }
}
</script>

<style lang="scss">
.finish-page {
  > h2, > p, > div {
    margin: 1em 10%;
  }
  .progress-goals {
    width: 22em;
    margin: 0px;
  }
  .social-icons {
    position: absolute;
    left: 50%;
    width: 10em;
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
  .footer {
    position: fixed;
    display: block;
    margin: 0px;
    bottom: 0px;
    left: 0px;
    padding: 0 0 2em 0;
    width: 100%;
    text-align: center;
    z-index: 1000;
    background: white;
    a { display: inline-block; margin: 0px; height: 2em; padding: 0px;  }
  }
}
</style>
