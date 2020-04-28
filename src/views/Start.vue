<template lang="pug">
div
  h1 Streetwise Crowdsourcing
  h2 Hallo! Schön, dass du hier bist.
  p Wir alle fühlen uns am unterschiedlichen Orten mehr oder weniger sicher. Wie sicher fühlst du dich an einem öffentlichen Platz, an einer dicht befahrenen Strasse oder in einer Sackgasse?
  a(href="https://streetwise.space")
    vs-button(flat) Hier findest du mehr Infos zum Projekt Streetwise
  | &nbsp;
  router-link(to="/wise")
    vs-button(flat) Hier geht's zur Umfrage. Mach mit und gewinne ein iPhone!
</template>

<script>
export default {
  name: 'tour',
  components: {
  }
}
</script>

<style lang="scss">

</style>
