<template lang="pug">
.start
  h1
    span.material-icons emoji_people
    span.smaller Willkommen zum Crowdsourcing!
  p.lead
    | Bald gibt es die erste Karte der Schweiz, die deine Wahrnehmung des öffentlichen Raumes abbildet. Wie nimmst du deinen Lebensraum wahr? Wo fühlst du dich sicher, wo fühlst du dich gut?
  p.lead
    | Zeig es uns in dieser Umfrage und mach mit beim Wettbewerb eines iPhone 11. Die Umfrage dauert max. 5 Minuten.
  .infobox
    center
      img.icon(src="@/assets/icons/road.svg")
      img.icon(src="@/assets/icons/road2.svg")
      img.icon(src="@/assets/icons/nature.svg")
    p.campaign
      | Stell dir vor, du betrachtest die Bilder aus der Perspektive als Fussgänger*in, Skater*in, Trottinett- oder Velofahrer*in.
    p.tip
      vs-icon(icon="star", size="small", color="darkblue")
      | Wir zeigen dir Bildpaare und du schätzt ein, in welcher Umgebung du dich sicherer fühlen würdest. Tippe auf ein Bild, um es zu vergrössern.
    p.tip
      vs-icon(icon="star", size="small", color="darkblue")
      | Klicke entsprechend links oder rechts für deine Auswahl. Kannst du dich nicht entscheiden? Dann wähle «unentschieden».
    p.tip
      vs-icon(icon="star", size="small", color="darkblue")
      span Ein kleiner Tipp als Handy-Nutzer*in: halte das Handy quer für eine bessere Ansicht!
    router-link.wiselink(to="/wise")
      vs-button(flat) Hier geht es zur Umfrage
  center
    a(href="https://streetwise.space/about", target="_blank" title="Mehr erfahren zum Projekt auf streetwise.space")
      img.logo(src="@/assets/streetwise_Logo.png")
    .credit Ein Kooperationsprojekt der <a href="https://www.metropolitanraum-zuerich.ch/themen/kooperationsprogramm-2019-2022/streetwise.html" target="_blank">Metropolitankonferenz&nbsp;Zürich</a>
    //vs-button(flat, color="black") Mehr zu&nbsp;
      b Streetwise
  center(style="margin-top:2em")
    .together
      span Fragen?&nbsp;
      a(href="mailto:hallo@streetwise.space") hallo@streetwise.space
      span.material-icons email
    .together
      span Bemerkungen zur Umfrage?&nbsp;
      a(href="https://forms.gle/fDcXHYkSire7GRiU9", target="_blank") Feedback
      span.material-icons event_available
    ul.attribution
      li Code (MIT) von <a href="https://github.com/Streetwise/" target="_blank" title="GitHub">Streetwise team</a>.
      li Bilder (CC BY-SA) von <a href="https://www.mapillary.com/" target="_blank">Mapillary</a>.
      li Icons (FlatIcon) von <a href="https://www.flaticon.com/authors/vitaly-gorbachev" title="Vitaly Gorbachev" target="_blank">Vitaly Gorbachev</a>.
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
    color: #444;
    font-size: 80%;
    font-weight: normal;
  }
}
.together { white-space: nowrap; }
p { text-align: left; }
p.lead, p.campaign { font-size: 120%; }
p.campaign { color: darkblue; font-weight: bold; }
p.tip .vs-icon { float: left; margin-bottom: 2em; margin-right: 0.2em; }
img.logo {
  max-width: 80%;
}
img.icon {
  width: 50px; margin: 10px;
  &.left { float:left; margin-right: 1em; }
  &.right { float:right; margin-left: 2em;  }
}
center { margin-top: 1em; }
.lead, .infobox {
  margin: 0 20% 1em;
}
.infobox {
  border: 1px dashed blue;
  padding: 1em;
}
.credit {
  font-size: 90%;
  color: black;
  & a { color: black; text-decoration: underline; }
}
.attribution {
  font-size: 80%;
  color: #555;
  text-align: center;
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
