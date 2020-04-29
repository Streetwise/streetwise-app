<template lang="pug">
div
  h1 Streetwise Crowdsourcing
  h2 Hallo! Schön, dass du hier bist.
  p Wir alle fühlen uns am unterschiedlichen Orten mehr oder weniger sicher. Wie sicher fühlst du dich an einem öffentlichen Platz, an einer dicht befahrenen Strasse oder in einer Sackgasse?
  a(href="https://streetwise.space")
    vs-button(flat) Hier findest du mehr Infos zum Projekt Streetwise
  router-link(to="/wise")
    vs-button(flat) Hier geht's zur Umfrage. Mach mit und gewinne ein iPhone!

  p(style="margin-top:2em")
    span Fragen? 👉&nbsp;
    a(href="mailto:hallo@streetwise.space") hallo@streetwise.space
</template>

<script>
export default {
  name: 'Start',
  components: {
  }
}
</script>

<style lang="scss" scoped>
h1, h2, p { margin: 1em; }
.vs-button {
  font-size: 150%;
  margin: 0.5em;
}
</style>
