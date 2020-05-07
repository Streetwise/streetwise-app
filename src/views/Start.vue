<template lang="pug">
.start
  img.logo(src="@/assets/streetwise_Logo.png")
  h1
    span.material-icons emoji_people
    span.smaller Hallo! Schön, dass du hier bist.
  p.lead
    img.icon.right(src="@/assets/icons/road.svg")
    | Bald gibt es die erste Karte der Schweiz, die deine Wahrnehmung des öffentlichen Raumes abbildet. Wie nimmst du deinen Lebensraum wahr? Wo fühlst du dich sicher, wo fühlst du dich gut?
  p
    img.icon.right(src="@/assets/icons/road2.svg")
    b So funktioniert’s
  p
    | Die folgende Umfrage fragt zunächst nach deinem allgemeinen Sicherheitsempfinden. Wir zeigen dir Bildpaare und du schätzt ein, in welcher Umgebung du dich sicherer fühlen würdest.
    b &nbsp;Stell dir vor, du betrachtest die Bilder aus der Perspektive als Fussgängerin, Skater, Trottinett- oder Velofahrer.
    | &nbsp;Scrolle oder tippe auf ein Bild, um es zu vergrössern. Klicke entsprechend auf links oder rechts für deine Auswahl. Kannst du dich nicht entscheiden? Dann wähle «beide / weiss nicht».
  p.campaign
    | Wir zeigen dir Bildpaare und du schätzt ein, in welcher Umgebung du dich sicherer fühlen würdest.
  p
    img.icon.right(src="@/assets/icons/nature.svg")
    | Drücke entsprechend auf <b>Links</b> bzw. <b>Rechts</b>. Zu schwierig zu entscheiden? Wähle <b>Unsicher</b>.
    | Tippe auf ein Bild, um es in <b>Vollbild</b> anzuschauen.
    | Bitte beantworte <b>mindestens 10</b> Bildpaare.
  router-link.wiselink(to="/wise")
    vs-button(flat) Hier geht es zur Umfrage.
  center(style="margin:0px")
    b Mach bei der Umfrage mit und&nbsp;
    a.together(href="https://streetwise.space/disclaimer", target="_blank") gewinne ein iPhone 11
  br
  a(href="https://streetwise.space", target="_blank")
    vs-button(flat, color="default") Worum geht es bei&nbsp;
      b Streetwise?
  center
    .together
      span Fragen?&nbsp;
      a(href="mailto:hallo@streetwise.space") hallo@streetwise.space
      span.material-icons email
    .together
      span Bemerkungen?&nbsp;
      a(href="https://forms.gle/fDcXHYkSire7GRiU9", target="_blank") Feedback
      span.material-icons event_available
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
h1 {
  color: black;
  .material-icons {
    font-size: 120%;
    vertical-align: middle;
  }
  .smaller {
    color: #444; padding-left: 1em;
    font-size: 80%; font-weight: normal;
  }
}
.together { white-space: nowrap; }
p { text-align: left; margin: 0 20% 1em; }
p.lead, p.campaign { font-size: 120%; }
p.campaign { color: darkblue; font-weight: bold; }
img.logo {
  max-width: 80%;
}
img.icon {
  width: 50px; margin-bottom: 2em;
  &.left { float:left; margin-right: 1em; }
  &.right { float:right; margin-left: 2em;  }
}
center { margin-top: 2em; }
.attribution {
  font-size: 80%;
  color: #555;
  text-align: right;
  margin: 3em;
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
