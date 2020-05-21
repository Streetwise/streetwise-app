<template>
  <div class="imagevote">
    <div class="progressbar">
      <vs-progress :height="12" :percent="votePercent" color="warning"></vs-progress>
    </div>

    <h3 class="lead">{{ msg }}</h3>

    <div>
      <ImagePair v-bind:leftImage=this.leftImage v-bind:rightImage=this.rightImage v-bind:voteLeft="voteLeft" v-bind:voteRight="voteRight" />
    </div>

    <div v-if=this.areImagesInvalid>{{this.onImageError()}}</div>

    <div class="vote-buttons">
      <vs-button flat size="large" color="success" class="vote left" @click.prevent="voteLeft">links</vs-button>
      <vs-button flat size="large" color="warning" class="undecided" @click.prevent="openUndecided=true">unentschieden</vs-button>
      <vs-button flat size="large" color="success" class="vote right" @click.prevent="voteRight">rechts</vs-button>
    </div>
    <IssueBox :active="openUndecided" v-on:close-box="voteUndecided($event)" />
    <p class="vote-count" v-show="debug">{{ voteCount }} / {{ voteRequired }}</p>
    <p style="margin:1em" v-show="debug">
      <vs-button type="line" color="rgb(200,200,200)" @click.prevent="voteSkip">Überspringen</vs-button>
    </p>
  </div>
</template>

<script>
import $backend from '@/backend'
import IssueBox from '@/components/IssueBox.vue'
import ImagePair from '@/components/ImagePair.vue'

export default {
  name: 'ImageVote',
  props: {
    msg: String,
    skipintro: Boolean
  },
  components: {
    IssueBox,
    ImagePair
  },
  computed: {
    // Reactive computed values from the vuex store
    leftImage () { return this.$store.state.images.left.url },
    rightImage () { return this.$store.state.images.right.url },
    leftImageId () { return this.$store.state.images.left.id },
    rightImageId () { return this.$store.state.images.right.id },
    areImagesInvalid () { return this.$store.state.images.invalid }
  },
  data () {
    return {
      voteRequired: 10, // number of images to require
      resources: [], // response from voting
      session: null, // current session
      debug: false,
      timeStart: Date.now(),
      voteCount: 0,
      voteTotal: 0,
      votePercent: 0,
      popupImage: false,
      popupLeft: false,
      openUndecided: false
    }
  },
  methods: {
    elapsedTime () {
      return Math.round((Date.now() - this.timeStart) / 1000)
    },
    checkVotesComplete () {
      if (this.voteCount === this.voteRequired) {
        if (this.skipintro) {
          let voter = this
          this.$vs.dialog({
            type: 'alert',
            color: 'success',
            title: `Weiter geht es`,
            text: 'Danke für deine Eingaben! Du kannst nun 10 weitere Bildpaaren beurteilen.',
            acceptText: 'Bestätigen',
            accept: function () {
              // Continue responding to questions
              voter.voteCount = 0
            },
            cancel: function () {
              // Return to home screen
              voter.$router.push({ name: 'finish' })
            }
          })
        } else {
          // Continue to finish survey screen
          this.$router.push({ name: 'complete', params: { responses: this.voteTotal } })
        }
      }
      return false
    },
    onImageError () {
      let self = this
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: `Verbindungsfehler`,
        text: 'Zurzeit kann keine Verbindung hergestellt werden. Überprüfen Sie bitte das Netzwerk und versuchen Sie es später erneut.',
        acceptText: 'Bestätigen',
        cancelText: 'Abbrechen',
        accept: function () {
          self.voteCount--
          self.voteTotal--
          self.nextImagePair()
          console.log(self)
        },
        cancel: function () {
          self.$router.push({ name: 'finish' })
        }
      })
    },
    nextImagePair (skip = false) {
      if (!skip) {
        this.voteCount++
        this.voteTotal++
        this.votePercent = 100 * this.voteCount / this.voteRequired
        if (this.checkVotesComplete()) { return }
      }
      this.timeStart = Date.now()
      this.$store.dispatch('refreshImages')
    },
    vote (isRight, textComment = '') {
      // Reset images to the initial loading state
      this.$store.commit('resetImages')
      $backend.voteCast(
        isRight,
        this.leftImageId,
        this.rightImageId,
        this.elapsedTime(),
        textComment
      )
        .then(responseData => {
          if (responseData === null) {
            return this.$vs.notify({ text: 'Das ging etwas zu schnell.', color: 'warning', position: 'top-center' })
          }
          this.session = responseData.session_hash
          this.resources.push(responseData)
          this.nextImagePair()
        }).catch(error => {
          console.warn(error.message)
          if (error.message.indexOf('429')) {
            this.$vs.notify({ text: 'Bitte wiederhole deine Eingabe.', color: 'warning', position: 'top-center' })
          } else {
            this.$vs.notify({ text: 'Es gab einen Fehler bei der Übermittlung.', color: 'danger', position: 'top-center' })
          }
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
  },
  mounted () {
    this.nextImagePair()
  }
}
</script>

<style scoped lang="scss">
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
@media screen and (max-height: 900px) and (min-height: 700px) {
  .progressbar { top: 0px; }
}
@media screen and (max-height: 700px) and (min-height: 601px) {
  .progressbar { top: 0px; }
}
@media screen and (max-height: 600px) and (min-height: 401px) {
  .progressbar { top: 0px; }
}
@media screen and (max-height: 500px) and (min-width: 640px) {
  .progressbar { margin: 0.5em 0 0 !important; }
}
@media screen and (max-height: 400px) {
  .progressbar { top: 0px; }
}

.lead {
  padding: 0.5em;
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
    min-width: 5em;
    width: 40%;
    font-weight: bold;
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
  right: 0px;
  p {
    display: none;
  }
  div {
    width: 10em;
  }
}
</style>
