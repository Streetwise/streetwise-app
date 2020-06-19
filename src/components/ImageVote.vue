<template>
  <div class="imagevote">
    <div class="progressbar">
      <vs-progress :height="12" :percent="votePercent" color="warning"></vs-progress>
    </div>

    <h3 class="lead" :style="msgStyle">{{ msg }}</h3>

    <div class="imagepane">
      <div class="left" @click="popupImage=true;popupLeft=true" ref="leftImagePane">
        <ImageContainer v-bind:errorHandler="this.promptNetworkError" v-bind:source="imageLeftUrl" />
      </div>
      <div class="right" @click="popupImage=true;popupLeft=false" ref="rightImagePane">
        <ImageContainer v-bind:errorHandler="this.promptNetworkError" v-bind:source="imageRightUrl" />
      </div>
    </div>

    <vs-popup fullscreen
      classContent="lightbox-container" styleHeader="display:none"
      :active.sync="popupImage" @close="popupImage=false"
      :title="`${popupLeft ? 'linkes Bild' : 'rechtes Bild'}`">
      <div class="lightbox" @click="popupImage=false"
        :style="{ backgroundImage: `url(${popupLeft ? imageLeftUrl : imageRightUrl})`  }"
      >
        <div class="buttons">
          <vs-button class="back-btn" flat size="large" color="dark" type="border" @click="popupImage=false">zurück</vs-button>
          <vs-button v-show="popupLeft" flat size="large" color="success" @click.prevent="voteLeft">Bild auswählen</vs-button>
          <vs-button v-show="!popupLeft" flat size="large" color="success" @click.prevent="voteRight">Bild auswählen</vs-button>
          <vs-button flat size="large" color="warning" class="undecided" @click.prevent="openUndecided=true">unentschieden</vs-button>
        </div>
      </div>
    </vs-popup>
    <div class="vote-buttons">
      <vs-button flat size="large" color="success" class="vote left" @click.prevent="voteLeft"><b>linkes</b>&nbsp;Bild</vs-button>
      <vs-button flat size="large" color="warning" class="undecided" @click.prevent="openUndecided=true">unentschieden</vs-button>
      <vs-button flat size="large" color="success" class="vote right" @click.prevent="voteRight"><b>rechtes</b>&nbsp;Bild</vs-button>
    </div>
    <IssueBox :active="openUndecided" v-on:close-box="voteUndecided($event)" />
    <p class="vote-count" v-show="debugmode">{{ voteCount }} / {{ votesrequired }}</p>
    <p style="margin:1em" v-show="debugmode">
      <vs-button type="line" color="light" @click.prevent="voteSkip">Überspringen</vs-button>
    </p>
  </div>
</template>

<script>
import $backend from '@/backend'
import IssueBox from '@/components/IssueBox.vue'
import ImageContainer from '@/components/ImageContainer.vue'

const imageLoading = '/images/loading.gif'

export default {
  name: 'ImageVote',
  props: {
    msg: String,
    skipcomplete: Boolean,
    skipfeedback: Boolean,
    debugmode: {
      type: Boolean,
      default: false
    },
    votesrequired: {
      type: Number,
      default: 10
    },
    campaign: {
      type: Number,
      default: null
    },
    msgStyle: {
      type: String,
      default: 'border-color:white'
    }
  },
  components: {
    IssueBox,
    ImageContainer
  },
  data () {
    return {
      resources: [], // response from voting
      session: null, // current session
      imageLeft: 0,
      imageRight: 0,
      imageLeftUrl: imageLoading,
      imageRightUrl: imageLoading,
      timeStart: Date.now(),
      voteCount: 0,
      voteTotal: 0,
      votePercent: 0,
      popupImage: false,
      popupLeft: false,
      openUndecided: false,
      errorPromptVisible: false
    }
  },
  watch: {
    campaign: function (val) {
      // Wait for campaign id to propagate before initializing
      if (val !== null && !this.hasLoaded()) this.nextImagePair()
    }
  },
  mounted: function () {
    // Init immediately if campaign data is available
    if (this.campaign !== null && !this.hasLoaded()) this.nextImagePair()
  },
  methods: {
    elapsedTime () {
      return Math.round((Date.now() - this.timeStart) / 1000)
    },
    hasLoaded () {
      return this.imageLeft !== 0 && this.imageRight !== 0
    },
    checkVotesComplete () {
      if (this.voteCount >= this.votesrequired) {
        if (this.skipcomplete && this.skipfeedback) {
          const voter = this
          this.voteCount = 0
          this.$vs.dialog({
            type: 'alert',
            color: 'success',
            title: `Weiter geht es`,
            text: 'Danke für deine Eingaben! Du kannst nun 10 weitere Bildpaaren beurteilen.',
            acceptText: 'Bestätigen',
            accept: function () {
              // Continue responding to questions
            },
            cancel: function () {
              // Return to home screen
              voter.$router.push({ name: 'start' })
            }
          })
        } else if (this.skipcomplete) {
          // Continue to feedback screen
          this.$router.push({ name: 'complete', params: { skipsurvey: true, responses: this.voteTotal } })
        } else {
          // Continue to finish survey screen
          this.$router.push({ name: 'complete', params: { responses: this.voteTotal } })
        }
      }
      return false
    },
    promptNetworkError () {
      if (this.errorPromptVisible) return
      this.errorPromptVisible = true
      const self = this
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: `Verbindungsfehler`,
        text: 'Zurzeit kann keine Verbindung hergestellt werden. Überprüfen Sie bitte das Netzwerk und versuchen Sie es später erneut.',
        acceptText: 'Bestätigen',
        cancelText: 'Abbrechen',
        accept: function () {
          self.errorPromptVisible = false
          self.nextImagePair(true)
        },
        cancel: function () {
          self.errorPromptVisible = false
          self.$router.push({ name: 'start', query: { 'reason': 'net_err' } })
        }
      })
    },
    nextImagePair (skip = false) {
      if (this.campaign === null || this.campaign === 'null') {
        console.info('Waiting for campaign data')
        return
      }
      if (!skip) {
        this.voteCount++
        this.voteTotal++
        this.votePercent = 100 * this.voteCount / this.votesrequired
        if (this.checkVotesComplete()) { return }
      }
      this.timeStart = Date.now()
      this.imageLeftUrl = imageLoading
      this.imageRightUrl = imageLoading
      this.$refs.leftImagePane.scrollLeft = 200
      this.$refs.rightImagePane.scrollLeft = 200
      $backend.getRandomImages()
        .then(responseData => {
          // console.debug(responseData)
          this.imageLeft = responseData[0].id
          this.imageLeftUrl = responseData[0].Url
          this.imageRight = responseData[1].id
          this.imageRightUrl = responseData[1].Url
        }).catch((error) => this.promptNetworkError(error))
    },
    promptVoteTooFast () {
      this.$vs.dialog({
        type: 'alert',
        color: 'warning',
        title: 'Upps!',
        text: 'Das ging etwas zu schnell.',
        acceptText: 'wiederholen'
      })
    },
    vote (isRight, textComment = '') {
      $backend.voteCast(
        isRight,
        this.imageLeft,
        this.imageRight,
        this.elapsedTime(),
        textComment
      )
        .then(responseData => {
          if (responseData === null) {
            return this.promptVoteTooFast()
          }
          this.session = responseData.session_hash
          this.resources.push(responseData)
          this.nextImagePair()
        }).catch(error => {
          if (error.message.indexOf('429') !== -1) {
            return this.promptVoteTooFast()
          }
          this.$vs.notify({ text: 'Es gab einen Fehler bei der Übermittlung.', color: 'danger', position: 'top-center' })
        })
    },
    voteLeft () {
      this.vote(false)
    },
    voteRight () {
      this.vote(true)
    },
    voteUndecided (accept) {
      this.openUndecided = false
      if (accept === false) return
      this.$vs.notify({ text: 'Danke für deine Rückmeldung.', color: 'warning', position: 'top-center' })
      this.vote(null, accept)
    },
    voteSkip () {
      this.nextImagePair(true)
      this.$vs.notify({ text: 'Übersprungen!', color: 'warning', position: 'top-center' })
    }
  } // -methods
}
</script>

<style scoped lang="scss">
.imagepane {
  text-align: center;
  width: 100%;
  overflow: hidden;
  div {
    display: inline-block;
    width: 50%;
    height: 60%;
    padding: 0px; margin: 0px;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
    overflow-y: hidden;
    overflow-x: scroll;
    img {
      padding: 0px; border: 0px; margin: 0px;
    }
  }
}

@media screen and (max-width: 600px) {
  .vs-button.complain {
    margin-top: 9px;
    background: white;
  }
  .imagevote .lead {
    font-size: 90%;
    position: relative;
    margin: 0.3em;
    left: 0px;
  }
}

/* Vertical positioning of images */
@media screen and (min-height: 1200px) {
  .imagepane div img { height: 1000px; }
}
@media screen and (max-height: 1200px) and (min-height: 900px) {
  .imagepane div img { height: 660px; }
}
@media screen and (max-height: 900px) and (min-height: 700px) {
  .imagepane div img { height: 500px; }
}
@media screen and (max-height: 700px) and (min-height: 601px) {
  .imagepane div img { height: 400px; }
}
@media screen and (max-height: 600px) and (min-height: 401px) {
  .imagepane div img { height: 333px; }
}
@media screen and (max-height: 500px) and (min-width: 640px) {
  .imagepane div img { height: 260px;}
}
@media screen and (max-height: 400px) {
  .imagepane div img { height: 205px; }
}

.lightbox {
  width: 100%; height: 100%;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center center;
  overflow: hidden;
  .buttons {
    position: absolute;
    bottom: 2em;
    width: 100%; margin-left: -30px;
    text-align: center;
    z-index: 1000;
    button:first-child { margin-right: 10px; }
    .back-btn { background-color: white; }
  }
}

.lead {
  padding: 0.5em;
  border-top: 5px solid white;
}

@media screen and (max-height: 600px) {
  .vote-buttons {
    position: fixed;
    bottom: 0px;
  }
}
@media screen and (max-width: 600px) {
  .vote-buttons .vs-button.vote {
    width: 30% !important;
    padding: 12px 4px;
  }
}
.vote-buttons {
  width: 100%;
  z-index: 100;
  text-align: center;
  overflow: hidden;
  white-space: nowrap;
  margin: 0px; padding: 0px;
  .vs-button {
    border-radius: 0px;
    color: black;
    text-shadow: 1px 1px 1px white;
  }
  .vs-button.vote {
    width: 40%;
    min-width: 6em;
  }
  .vs-button.undecided {
    width: 18%;
    min-width: 8em;
  }
  .vs-button {
    border-right: 1px solid white;
  }
  .vs-button:last-child {
    border-right: none;
  }
}

/*
.vote-count {
  margin-top: 1em;
  color: #999;
}
*/

/*
.undecided {
  text-align: center;
  width: 100%;
  margin-top: 0.5em;
  button {
    padding: 0px 2em;
    z-index: 99;
    height: 2.8em;
    color: #000;
    font-weight: bold;
    text-shadow: 1px 1px 1px white;
  }
}
@media screen and (max-width: 600px) and (min-height: 400px) {
  .undecided button {
    margin: 0px;
  }
}
*/
.complain {
  position: absolute;
  &.left { left: 5px; }
  &.right { right: 5px; }
}

.progressbar {
  text-align: right;
  margin: 1em;
  border-radius: 5px;
  background: white;
  padding: 0 5px;
  position: absolute;
  top: 0px;
  right: 0px;
  p {
    display: none;
  }
  div {
    width: 10em;
  }
}
</style>
