<template lang="pug">
.start
  .infobox
    center
      img.icon(src="@/assets/icons/road.svg")
      img.icon(src="@/assets/icons/road2.svg")
      img.icon(src="@/assets/icons/nature.svg")
    p.campaign
      | Deine Wahrnehmung ist gefragt: schau dir auf den Bildern die ganze
      | Umgebung an und bewerte diese als Fussgänger*in oder Velofahrer*in.
    table
      tr
        td
          vs-icon(icon="star", size="small", color="darkblue")
        td
          | Tippe auf ein Bild, um es zu vergrössern. Klicke entsprechend links
          | oder rechts für deine Auswahl. Kannst du dich nicht entscheiden?
          | Dann wähle «unentschieden».
    ProgressGoals
    center.wiselink
      router-link(to="/wise")
        vs-button.start-button(flat, color="success", icon="arrow_forward_ios")
          span Zur&nbsp;Umfrage
  p.lead.contest
    | Mach mit bei der Verlosung eines iPhone&nbsp;11.
  p.lead
    b Die Umfrage dauert max. 5 Minuten.&#32;
    | Bald gibt es die erste Karte der Schweiz, die deine Wahrnehmung des öffentlichen Raumes abbildet. Wie nimmst du deinen Lebensraum wahr? Wo fühlst du dich sicher, wo fühlst du dich gut?&#32;
    router-link(to="/wise") Jetzt starten!
  center
    a(href="https://streetwise.space/about", target="_blank" title="Mehr erfahren zum Projekt auf streetwise.space")
      img.logo(src="@/assets/streetwise_Logo.png")
    .credit Ein Kooperationsprojekt der <a href="https://www.metropolitanraum-zuerich.ch/themen/kooperationsprogramm-2019-2022/streetwise.html" target="_blank">Metropolitankonferenz&nbsp;Zürich</a>
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
      li Icons (FlatIcon) von <a href="https://www.flaticon.com/authors/vitaly-gorbachev" target="_blank">Vitaly Gorbachev</a>.
      li Copyright &copy; 2020 <a href="https://streetwise.space/impressum" target="_blank">Streetwise ARGE</a>
</template>

<script>
import ProgressGoals from '@/components/ProgressGoals.vue'

export default {
  name: 'Start',
  components: {
    ProgressGoals
  },
  mounted () {
    localStorage.setItem('streetwiseSession', null)
    localStorage.setItem('currentCampaignId', null)
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
p { text-align: left; }
p.campaign { font-size: 120%; color: darkblue; font-weight: bold; }
img.logo {
  max-width: 80%;
}
img.icon {
  width: 50px; margin: 10px;
  &.left { float:left; margin-right: 1em; }
  &.right { float:right; margin-left: 2em;  }
}
center { margin-top: 1em; }
table, table td { border: 0px; text-align: left; vertical-align: top; }
table td { padding-bottom: 0.5em; padding-left: 1em; }
.lead, .infobox {
  margin: 0 20% 1em;
}
.contest {
  & a {
    color: darkblue;
    text-decoration: underline;
  }
  color: darkblue;
  clear: both;
  display: inline-block;
  padding: 0px 1em;
  text-align: center;
}
// .infobox {
//   border: 1px dashed blue;
//   padding: 1em;
// }
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
.wiselink .vs-button {
  float: none;
}
.start-button .vs-button--text { font-size: 150%; }
@media screen and (min-width: 800px) {
  .start { font-size: 125%; }
  p { line-height: 150%; }
  img.icon { width: 80px; }
  .wiselink a { clear: both; display: block; }
}
@media screen and (max-width: 800px) {
  .start-button { width: 100%; }
  .start-button .vs-icon { transform: scale(0.6); }
  .start-button .vs-button--text { font-size: normal; }
  .lead, .infobox { margin-left: 10%; margin-right: 10%; }
}
</style>
