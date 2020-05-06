<template>
  <div class="imagevote">
    <div class="progressbar">
      <p>{{ voteCount }} / {{ voteTotal }}</p>
      <vs-progress :height="12" :percent="votePercent" color="warning"></vs-progress>
    </div>

    <h4 class="lead">{{ msg }}</h4>

    <div class="imagepane">
      <div class="left" @click="popupImage=true;popupLeft=true">
        <img :src="imageLeftUrl">
      </div>
      <div class="right" @click="popupImage=true;popupLeft=false">
        <img :src="imageRightUrl">
      </div>
    </div>

    <vs-popup fullscreen
      classContent="lightbox-container" styleHeader="display:none"
      :active.sync="popupImage" @close="popupImage=false" title="Zoom">
      <div class="lightbox" @click="popupImage=false"
        :style="{ backgroundImage: `url(${popupLeft ? imageLeftUrl : imageRightUrl})`  }"
      >
        <div class="buttons">
          <vs-button flat size="large" color="black" @click="popupImage=false">Schliessen</vs-button>
          <vs-button v-show="popupLeft" flat size="large" color="success" @click.prevent="voteLeft">Bild auswählen</vs-button>
          <vs-button v-show="!popupLeft" flat size="large" color="success" @click.prevent="voteRight">Bild auswählen</vs-button>
        </div>
      </div>
    </vs-popup>

    <p class="undecided">
      <vs-button flat size="large" color="rgb(255,255,255)" @click.prevent="voteUndecided">Beide / Weiss nicht</vs-button>
    </p>
    <p>
      <vs-button flat size="large" color="success" class="vote left" @click.prevent="voteLeft">Links</vs-button>

      <vs-button flat size="large" color="success" class="vote right" @click.prevent="voteRight">Rechts</vs-button>
    </p>
    <p style="margin:1em" v-show="debug">
      <vs-button type="line" color="rgb(200,200,200)" @click.prevent="voteSkip">Überspringen</vs-button>
    </p>
  </div>
</template>

<script>
import $backend from '../backend'
export default {
  name: 'ImageVote',
  props: {
    msg: String,
    skipintro: Boolean
  },
  data () {
    return {
      voteTotal: 10, // number of images to require
      resources: [], // response from voting
      session: null, // current session
      debug: false,
      imageLeft: 0,
      imageLeftUrl: '/loading.gif',
      imageRight: 0,
      imageRightUrl: '/loading.gif',
      timeStart: Date.now(),
      voteCount: 0,
      votePercent: 0,
      popupImage: false,
      popupLeft: false
    }
  },
  methods: {
    elapsedTime () {
      return Math.round((Date.now() - this.timeStart) / 1000)
    },
    checkVotesComplete () {
      if (this.voteCount === this.voteTotal) {
        if (this.skipintro) {
          let voter = this
          this.$vs.dialog({
            type: 'alert',
            color: 'success',
            title: `Weiter geht es`,
            text: 'Danke für deine Eingaben! Du kannst nun 10 weitere Bildpaaren beurteilen.',
            accept: function () {
              voter.voteCount = 0
              voter.nextImagePair()
            },
            cancel: function () {
              // TODO: forward session
              voter.$router.push('complete')
            }
          })
        } else {
          // TODO: forward session
          this.$router.push('complete')
        }
      }
      return false
    },
    nextImagePair (skip = false) {
      if (!skip) {
        this.voteCount++
        this.votePercent = 100 * this.voteCount / this.voteTotal
        if (this.checkVotesComplete()) { return }
      }
      this.timeStart = Date.now()
      console.debug('Fetching image pair')
      $backend.getRandomImages()
        .then(responseData => {
          console.debug(responseData)
          this.imageLeft = responseData[0].id
          this.imageLeftUrl = responseData[0].Url
          this.imageRight = responseData[1].id
          this.imageRightUrl = responseData[1].Url
        })
    },
    vote (isRight) {
      $backend.voteCast(
        isRight,
        this.imageLeft,
        this.imageRight,
        this.elapsedTime(),
        this.session
      )
        .then(responseData => {
          if (responseData === null) {
            return this.$vs.notify({ text: 'Bitte nochmal wiederholen', color: 'warning', position: 'top-center' })
          }
          this.session = responseData.session_hash
          this.resources.push(responseData)
          this.nextImagePair()
        }).catch(error => {
          console.warn(error.message)
          if (error.message.indexOf('429')) {
            this.$vs.notify({ text: 'Bitte nochmal wiederholen', color: 'warning', position: 'top-center' })
          } else {
            this.$vs.notify({ text: 'Es gab einen Fehler', color: 'danger', position: 'top-center' })
          }
        })
    },
    voteLeft () {
      this.vote(false)
    },
    voteRight () {
      this.vote(true)
    },
    voteUndecided () {
      let voter = this
      this.$vs.dialog({
        type: 'confirm',
        color: 'warning',
        title: `Bestätigen`,
        text: 'Bitte bestätige, das du zwischen der beiden Situationen nicht entscheiden kannst.',
        accept: function () {
          voter.vote(null)
        }
      })
    },
    voteSkip () {
      this.nextImagePair(true)
      this.$vs.notify({ text: 'Übersprungen!', color: 'warning', position: 'top-center' })
    },
    complainImage () {
      let voter = this
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: `Problem melden`,
        text: 'Falls du den Bild nicht gut sehen kannst oder eine andere Problem melden willst, bitte im folgende Dialog kurz beschreiben. Wenn es um eine oder die beiden Bilder geht, bitte notiere um welchen es geht.',
        accept: function () {
          let note = prompt('Problem beschreiben:')
          if (note) {
            // TODO: needs API !
            voter.$vs.notify({ text: 'Danke fürs melden!', color: 'warning', position: 'top-center' })
          }
        }
      })
    }
  },
  mounted () {
    this.nextImagePair()
  }
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
    margin: 1em;
    left: 0px;
  }
}

/* Vertical positioning of images */
@media screen and (min-height: 1200px) {
  .imagepane div img { height: 1000px; }
}
@media screen and (max-height: 1200px) and (min-height: 900px) {
  .imagepane div img { height: 700px; }
}
@media screen and (max-height: 900px) and (min-height: 700px) {
  .imagepane div img { height: 500px; }
}
@media screen and (max-height: 700px) and (min-height: 601px) {
  .imagepane div img { height: 400px; }
}
@media screen and (max-height: 600px) {
  .imagepane div {
    img { height: 333px; }
  }
  .lead {
    display: none;
  }
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
    button { margin-right: 10px; }
  }
}

.lead {
  position: absolute;
  left: 50%;
  margin-left: -9em;
  margin-top: -2em;
}

.vs-button.vote {
  font-weight: bold;
  width: 5em;
  width: 50%;
  border: 1px solid white;
}

.undecided {
  text-align: center;
  width: 100%;
  button {
    z-index: 99;
    height: 2.8em;
    border-radius: 0px;
    position: absolute;
    color: #933;
    margin-left: -5em;
  }
}
@media screen and (max-width: 600px) {
  .undecided button {
      position: relative; margin: 0px;
      margin-top: -0.5em;
  }
}
.complain {
  position: absolute;
  &.left { left: 5px; }
  &.right { right: 5px; }
}

.progressbar {
  text-align: right;
  margin: 1em;
  p {
    position: absolute;
    right: 2.5em;
  }
  div {
    margin-right: 1em;
    width: 20%;
    min-width: 10em;
  }
}
</style>
