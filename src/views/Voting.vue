<template lang="pug">
.voting
  ImageVote(
    v-bind:msg='text.question',
    v-bind:campaign='campaignId',
    :debugmode='debugMode',
    :votesrequired='votesRequired',
    :skipcomplete='didSurvey',
    :skipfeedback='didFeedback',
    ref="imageVote")

  vs-popup(title='Hilfe', :active.sync='helpActive')
    .content.helpbox
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

export default {
  name: 'Voting',
  components: {
    ImageVote
  },
  props: {
    didSurvey: {
      type: Boolean,
      default: false
    },
    didFeedback: {
      type: Boolean,
      default: false
    },
    campaignId: {
      type: Number,
      default: null
    },
    campaignName: {
      type: String,
      default: null
    }
  },
  data () {
    return {
      text: {},

      // Orientation of app
      portraitMode: false,

      // Toggles state of dialogs
      helpActive: false,

      // Environment variable: number of images to require
      votesRequired: process.env.VUE_APP_VOTESREQUIRED || 10,
      // Environment variable: whether to show debug information
      debugMode: process.env.VUE_APP_DEBUG || false
    }
  },
  mounted () {
    if (this.campaignId === null || this.campaignName === null) {
      return this.$router.push({ name: 'wise', query: { 'reason': 'no_campaign' } })
    }
    this.text = CampaignTexts[this.campaignName].start
    this.showPortraitTip()
  },
  methods: {
    showPortraitTip () {
      this.portraitMode = window.matchMedia('(orientation: portrait)').matches && window.innerWidth < 768
      if (this.portraitMode) {
        this.$vs.notify({
          text: 'Ein kleiner Tipp: halte dein Handy quer für eine bessere Ansicht.',
          color: 'primary',
          position: 'bottom-center',
          time: 3000
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.helpbox {
  text-align: center;
  margin: 0 20%;
  font-size: 140%;
  > p, > div {
    text-align: left;
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
  .helpbox { font-size: normal; }
}
@media screen and (max-width: 600px) {
  .helpbox { font-size: initial; margin: 1em; }
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
