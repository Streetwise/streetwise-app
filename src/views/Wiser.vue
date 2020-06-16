<template lang="pug">
.wiser
  ImageVote(
    v-bind:msg='text.question',
    v-bind:campaign='campaignId',
    :debugmode='debugMode',
    :votesrequired='votesRequired',
    :skipcomplete='didsurvey',
    :skipfeedback='didfeedback',
    ref="imageVote")

  vs-popup(title='Info', :active.sync='infoActive', button-close-hidden)
    .content.centerx
      p(v-show="!didsurvey")
        | Für dich geht’s los mit der Frage:
      p(v-show="didsurvey")
        | Jetzt geht es weiter mit der Frage:
      h2 {{ text.question }}
      p {{ text.task }}
      p.tip
        div(v-html='text.hint')
      center
        vs-button(flat='', size='large', color='success', @click='infoActive=false;showTip()') alles klar

  vs-popup(title='Hilfe', :active.sync='helpActive')
    .content.centerx
      p.campaign
        div(v-html='text.hint')
      center.together
        | links &#x1F448;
        vs-button.undecided(disabled='', type='border', color='black') ???
        | &#x1F449; rechts
      p.tip
        | Tippe auf ein Bild, um es zu vergrössern. Klicke entsprechend auf links oder rechts für deine Auswahl. Kannst du dich nicht entscheiden? Dann wähle «unentschieden».
      p.tip.highlight(v-show="portraitMode")
        | Ein kleiner Tipp: halte dein Handy quer für eine bessere Ansicht der Bilder!
      center
        vs-button(flat='', size='large', color='success', @click='helpActive=false') Los geht&apos;s !
  center.help-icon
    vs-button(flat='', size='small', color='white', @click='helpActive=true', title='Anleitung')
      vs-icon(icon='help', size='small', bg='orange', round='')
      b Anleitung
</template>

<script>
import ImageVote from '@/components/ImageVote.vue'
import CampaignTexts from '@/texts/campaigns.yaml'
import $backend from '@/backend'

export default {
  name: 'Wiser',
  components: {
    ImageVote
  },
  props: {
    didsurvey: {
      type: Boolean,
      default: false
    },
    didfeedback: {
      type: Boolean,
      default: false
    },
    setcampaign: {
      type: Number,
      default: 1
    }
  },
  data () {
    return {
      text: {},
      campaignId: this.setcampaign,

      // Toggles state of dialogs
      infoActive: true,
      helpActive: false,

      // Shows notice about landscape mode
      portraitMode: false,

      // Environment variable: number of images to require
      votesRequired: process.env.VUE_APP_VOTESREQUIRED || 10,
      // Environment variable: whether to show debug information
      debugMode: process.env.VUE_APP_DEBUG || false
    }
  },
  mounted () {
    this.portraitMode = window.matchMedia('(orientation: portrait)').matches && window.innerWidth < 768
  },
  methods: {
    showTip () {
      if (this.portraitMode) {
        this.$vs.notify({
          text: 'Ein kleiner Tipp: halte dein Handy quer für eine bessere Ansicht.',
          color: 'primary',
          position: 'bottom-center',
          time: 5000
        })
      }
    }
  },
  beforeCreate: function () {
    const self = this
    $backend.getNextCampaign()
      .then((res) => {
        self.campaignId = res.id
        const selectContent = CampaignTexts[res.name]
        self.text = selectContent.start
        // console.info(selectContent.id, 'text loaded')
        // Trigger loading images from the selected campaign
        // self.$refs.imageVote.nextImagePair()
      })
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
.help-icon {
  z-index: 10000;
  b { color: orange !important; font-size: 120%; }
  button { padding: 7px; }
}
.highlight {
  color: black;
  background-color: yellow;
  padding: 0 5pt;
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
