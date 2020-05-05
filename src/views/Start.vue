<template lang="pug">
div
  img.logo(src="@/assets/streetwise_Logo.png")
  h1 Hallo
    span.material-icons emoji_people
  h3 Schön, dass du hier bist.
  p Wir alle fühlen uns am unterschiedlichen Orten mehr oder weniger sicher. Wie sicher fühlst du dich an einem öffentlichen Platz, an einer dicht befahrenen Strasse oder in einer Sackgasse?
  router-link(to="/wise")
    vs-button(flat) Hier geht es zur Umfrage.
  b Mach&nbsp;mit&nbsp;und&nbsp;
  a(href="https://streetwise.space/disclaimer", target="_blank") gewinne ein iPhone!
  br
  a(href="https://streetwise.space", target="_blank")
    vs-button(flat, color="black") Hier findest du mehr Infos zum&nbsp;
      b Projekt Streetwise
  center
    span.material-icons(style="margin:0 0.5em") email
    span Fragen?&nbsp;
    a(href="mailto:hallo@streetwise.space") hallo@streetwise.space
    span.material-icons(style="margin:0 0.5em") event_available
    span Bemerkungen?&nbsp;
    a(href="https://forms.gle/fDcXHYkSire7GRiU9", target="_blank") Feedback
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
.logo {
  max-width: 100%;
  width: 400px;
  margin: 20px;
}
@media screen and (max-width: 800px) {
  p { margin: 0 10%; }
}
</style>
