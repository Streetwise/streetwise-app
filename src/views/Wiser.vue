<template lang="pug">
.wiser
  ImageVote(msg='Wo fühlst du dich sicherer?', :skipintro='skipintro')
  vs-popup(title='Anleitungshilfe', :active.sync='popupActive')
    .content.centerx
      p.tip
        | Wir zeigen dir Bildpaare und du schätzt ein, in welcher Umgebung du dich sicherer fühlen würdest. Tippe auf ein Bild, um es zu vergrössern.
      center.together
        | links &#x1F448;
        vs-button.undecided(disabled='', type='border', color='black') ???
        | &#x1F449; rechts
      p.tip
        | Klicke entsprechend links oder rechts für deine Auswahl. Kannst du dich nicht entscheiden? Dann wähle «unentschieden».
      center
        vs-icon(icon="star", size="small", color="darkblue")
      p.tip
        span Ein kleiner Tipp als Handy-Nutzer*in: halte das Handy quer für eine bessere Ansicht!
      // <div><img style="max-width:100%" src="@/assets/example.jpg"></div>
      p
        | Bitte beantworte
        b &nbsp;mindestens 10
        | &nbsp;Bildpaare.
      center
        vs-button(flat='', size='large', color='success', @click='popupActive=false') Los geht&apos;s !
  center.help-icon
    vs-button(flat='', size='small', color='white', @click='popupActive=true', title='Anleitung')
      vs-icon(icon='help', size='small', bg='orange', round='')
      b Anleitung
</template>

<script>
import ImageVote from '@/components/ImageVote.vue'

export default {
  name: 'Wiser',
  components: {
    ImageVote
  },
  props: {
    skipintro: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      popupActive: false
    }
  },
  mounted () {
    // this.popupActive = !this.skipintro
  }
}
</script>

<style lang="scss" scoped>
.wiser {
  text-align: center;
}
.centerx {
  margin: 0 20%;
  font-size: 140%;
  p, div {
    margin: 1em 0;
  }
}
.lead {
  margin-top: 1em;
}
.together { white-space: nowrap; }
.help-icon {
  z-index: 10000;
  b { color: orange !important; font-size: 120%; }
  button { padding: 7px; }
}
.imagevote {
  margin-bottom: 7px;
}
@media screen and (max-height: 500px) {
  .centerx { font-size: normal; }
}
@media screen and (max-width: 600px) {
  .centerx { font-size: initial; margin: 1em; }
}
@media (max-height: 500px) and (min-width: 321px) {
  .help-icon {
    position: absolute;
    top: 0px; left: 50%;
    margin-left: -1.25em;
    b { display: none; }
  }
}
</style>
