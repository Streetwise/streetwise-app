<template lang="pug">
.wiser
  .content
    p(v-show='!didSurvey')
      | Für dich geht’s los mit der Frage:
    p(v-show='didSurvey')
      | Jetzt geht es weiter mit der Frage:
    h2(v-bind:style='cssBorderStyle')
      | {{ text.question }}
    p {{ text.task }}
    p.tip
      div(v-html='text.hint')
    center
      vs-button(
        flat='', size='large', color='success',
        @click='toVoting()') alles klar
    img.logo(
      v-show='imageurl'
      v-bind:src='imageurl',
      v-bind:style='cssBorderStyle',
    )
</template>

<script>
import CampaignTexts from '@/texts/campaigns.yaml'
import $backend from '@/backend'

export default {
  name: 'Wiser',
  props: {
    didSurvey: {
      type: Boolean,
      default: false
    },
    didFeedback: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      text: {},
      imageurl: null,
      cssBorderStyle: 'border-color:white',
      campaignId: null,
      campaignName: null
    }
  },
  methods: {
    toVoting () {
      if (this.campaignId === null) return
      this.$router.push({
        name: 'vote',
        params: {
          'didSurvey': this.didSurvey,
          'didFeedback': this.didFeedback,
          'campaignId': this.campaignId,
          'campaignName': this.campaignName
        }
      })
    }
  },
  beforeCreate: function () {
    const self = this
    $backend.getNextCampaign()
      .then((res) => {
        self.campaignId = res.id
        self.campaignName = res.name
        self.text = CampaignTexts[res.name]
        self.cssBorderStyle = 'border-color:' + self.text.color
        self.imageurl = require('@/assets/campaigns/' + self.text.image)
      })
  }
}
</script>

<style lang="scss" scoped>
.wiser {
  .content {
    text-align: center;
    margin: 0 20%;
    font-size: 140%;
    h2 {
      display: inline-block;
      border-bottom: 8px solid black;
    }
    > p, > div {
      margin: 1em 0;
    }
    img {
      border: 2px solid white;
      border-top: none;
      border-left: none;
      border-radius: 10px;
      box-shadow: 0px 0px 5px grey;
      padding: 5px;
      margin-top: 1em;
      width: 100%;
      max-width: 700px;
    }
  }
}
@media screen and (max-width: 600px) {
  .wiser .content { text-align: left; margin: 10%; }
}
</style>
