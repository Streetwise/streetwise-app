<template lang="pug">
.wiser
  .content
    p(v-show="!didSurvey")
      | Für dich geht’s los mit der Frage:
    p(v-show="didSurvey")
      | Jetzt geht es weiter mit der Frage:
    h2 {{ text.question }}
    p {{ text.task }}
    p.tip
      div(v-html='text.hint')
    center
      vs-button(flat='', size='large', color='success', @click='toVoting()') alles klar
    img.logo(src="@/assets/ui-sketch.png", v-show="!didSurvey")
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
        self.text = CampaignTexts[res.name].start
      })
  }
}
</script>

<style lang="scss" scoped>
.wiser {
  .content {
    margin: 0 20%;
    font-size: 140%;
    > p, > div {
      margin: 1em 0;
      text-align: left;
    }
    img {
      margin-top: 1em;
      width: 100%;
    }
  }
}
</style>
