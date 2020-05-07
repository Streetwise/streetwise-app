<template lang="pug">
.start
  img.logo(src="@/assets/streetwise_Logo.png")
  h1
    span.material-icons emoji_people
    span Hallo
    span.smaller.together Schön, dass du hier bist.
  p.lead
    img.icon.right(src="@/assets/icons/road.svg")
    | Es gibt tausende Karten – keine zeigt die Raumqualität aus Sicht der Bevölkerung. Wie nehmen wir unseren Lebensraum wahr? Wie erleben wir die Atmosphäre eines Ortes, wo fühlen wir uns sicher, wo fühlen wir uns gut? Diese Fragen werden umso wichtiger, je mehr Menschen in städtischen Gebieten leben.
  p
    img.icon.right(src="@/assets/icons/road2.svg")
    | Wir alle fühlen uns am unterschiedlichen Orten mehr oder weniger sicher. Wie sicher fühlst du dich an einem öffentlichen Platz, an einer dicht befahrenen Strasse oder in einer Sackgasse?
  p.campaign
    | Wir zeigen dir Bildpaare und du schätzt ein, in welcher Umgebung du dich sicherer fühlen würdest.
  p
    img.icon.right(src="@/assets/icons/nature.svg")
    | Drücke entsprechend auf <b>Links</b> bzw. <b>Rechts</b>. Zu schwierig zu entscheiden? Wähle <b>Beide / Weiss nicht</b>.
    | Tippe auf ein Bild, um es in <b>Vollbild</b> anzuschauen.
    | Bitte beantworte <b>mindestens 10</b> Bildpaare.
  router-link.wiselink(to="/wise")
    vs-button(flat) Hier geht es zur Umfrage.
  .together
    b Mach mit und&nbsp;
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
    ul.attribution
      li Ein Projekt der <a href="metropolitanraum-zuerich.ch/" target="_blank">Verein Metropolitanraum Zürich</a>
      li Code (MIT) by <a href="https://github.com/Streetwise/" target="_blank" title="GitHub">Streetwise team</a> &amp; contributors.
      li Imagery (CC BY-SA) by <a href="https://www.mapillary.com/" target="_blank">Mapillary</a> &amp; contributors.
      li Icons (FlatIcon) by <a href="https://www.flaticon.com/authors/vitaly-gorbachev" title="Vitaly Gorbachev" target="_blank">Vitaly Gorbachev</a>.
      li Copyright &copy; 2020 Streetwise ARGE
</template>

<script>
export default {
  name: 'Start',
  components: {
  },
  mounted () {
    localStorage.setItem('streetwiseSession', null)
  }
}
</script>

<style lang="scss" scoped>
h1, h2, h3, p { margin: 1em; }
h1 { color: black; }
h1 .material-icons { padding-right: 0.21em; font-size: 120%; vertical-align: middle; }
h1 .smaller {
  color: #444; padding-left: 1em;
  font-size: 80%; font-weight: normal;
}
.together { white-space: nowrap; }
p { text-align: left; margin: 0 20% 1em; }
p.lead, p.campaign { font-size: 120%; }
p.campaign { color: darkblue; font-weight: bold; }
img.icon {
  width: 50px; margin-bottom: 2em;
  &.left { float:left; margin-right: 1em; }
  &.right { float:right; margin-left: 2em;  }
}
center { margin-top: 2em; }
.attribution {
  font-size: 80%;
  color: #555;
  text-align: left;
  margin-top: 3em;
  width: 40em;
  margin-left: 20em;
  left: 50%;
  list-style: none;
}
.vs-button {
  font-size: 150%;
  margin: 0.5em;
}
.logo {
  max-width: 100%;
  width: 400px;
  margin: 20px;
}
@media screen and (min-width: 800px) {
  .start { font-size: 125%; }
  p { line-height: 150%; }
  img.icon { width: 80px; }
  .wiselink { clear: both; display: block; }
}
@media screen and (max-width: 800px) {
  p { margin-left: 10%; margin-right: 10%; }
}
</style>
