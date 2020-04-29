<template lang="pug">
div
  h1 Streetwise Crowdsourcing
  h2 Hallo
    span.material-icons emoji_people
  h3 Schön, dass du hier bist.
  p Wir alle fühlen uns am unterschiedlichen Orten mehr oder weniger sicher. Wie sicher fühlst du dich an einem öffentlichen Platz, an einer dicht befahrenen Strasse oder in einer Sackgasse?
  router-link(to="/wise")
    vs-button(flat) Hier geht es zur Umfrage.
  b Mach&nbsp;mit&nbsp;und gewinne ein iPhone!
  br
  a(href="https://streetwise.space")
    vs-button(flat, color="black") Hier findest du mehr Infos zum&nbsp;
      b Projekt Streetwise

  center
    span Fragen?&nbsp;
    a(href="mailto:hallo@streetwise.space") hallo@streetwise.space
    span.material-icons(style="margin:0 0.5em") email
    span Bemerkungen?&nbsp;
    a(href="https://forms.gle/fDcXHYkSire7GRiU9") Feedback
</template>

<script>
export default {
  name: 'Start',
  components: {
  }
}
</script>

<style lang="scss" scoped>
h1 { color: black; }
h1, h2, h3, p { margin: 1em; }
p { text-align: left; margin: 0 20%; }
center { margin-top: 2em; }
.vs-button {
  font-size: 150%;
  margin: 0.5em;
}
@media screen and (max-width: 800px) {
  p { margin: 0 10%; }
}
</style>
