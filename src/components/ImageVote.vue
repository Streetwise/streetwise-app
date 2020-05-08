<template>
  <div class="imagevote">
    <div class="progressbar">
      <vs-progress :height="12" :percent="votePercent" color="warning"></vs-progress>
    </div>

    <h3 class="lead">{{ msg }}</h3>

    <div class="imagepane">
      <div class="left" @click="popupImage=true;popupLeft=true" ref="leftImagePane">
        <img :src="imageLeftUrl">
      </div>
      <div class="right" @click="popupImage=true;popupLeft=false" ref="rightImagePane">
        <img :src="imageRightUrl">
      </div>
    </div>

    <vs-popup fullscreen
      classContent="lightbox-container" styleHeader="display:none"
      :active.sync="popupImage" @close="popupImage=false"
      :title="`${popupLeft ? 'Linkes Bild' : 'Rechtes Bild'}`">
      <div class="lightbox" @click="popupImage=false"
        :style="{ backgroundImage: `url(${popupLeft ? imageLeftUrl : imageRightUrl})`  }"
      >
        <div class="buttons">
          <vs-button flat size="large" color="black" @click="popupImage=false">Zurück</vs-button>
          <vs-button v-show="popupLeft" flat size="large" color="success" @click.prevent="voteLeft">Dieses Bild auswählen</vs-button>
          <vs-button v-show="!popupLeft" flat size="large" color="success" @click.prevent="voteRight">Dieses Bild auswählen</vs-button>
        </div>
      </div>
    </vs-popup>
    <p>
      <vs-button flat size="large" color="success" class="vote left" @click.prevent="voteLeft">links</vs-button>
      <vs-button flat size="large" color="success" class="vote right" @click.prevent="voteRight">rechts</vs-button>
    </p>
    <p class="undecided">
      <vs-button flat size="large" color="warning" @click.prevent="voteUndecided">unentschieden</vs-button>
    </p>
    <p style="margin:1em" v-show="debug">
      <vs-button type="line" color="rgb(200,200,200)" @click.prevent="voteSkip">Überspringen</vs-button>
    </p>
    <p class="vote-count">{{ voteCount }} / {{ voteTotal }}</p>
  </div>
</template>

<script>
import $backend from '../backend'
const imageLoading = '/images/loading.gif'
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
      imageRight: 0,
      imageLeftUrl: imageLoading,
      imageRightUrl: imageLoading,
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
    voteUndecided () {
      let voter = this
      this.$vs.dialog({
        type: 'confirm',
        color: 'warning',
        title: `Bestätigen`,
        text: 'Kannst du dich bei diesem Bildpaar wirklich nicht entscheiden, wo du dich sicherer fühlen würdest? Hast du Probleme mit der Ansicht eines Bildes?',
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
    margin: 0.3em;
    left: 0px;
  }
}

/* Vertical positioning of images */
@media screen and (min-height: 1200px) {
  .imagepane div img { height: 1000px; }
  .vote-count { position: absolute; right: 10px; top: 0px; }
}
@media screen and (max-height: 1200px) and (min-height: 900px) {
  .imagepane div img { height: 700px; }
  .vote-count { position: absolute; right: 10px; top: 0px; }
}
@media screen and (max-height: 900px) and (min-height: 700px) {
  .imagepane div img { height: 480px; }
  .progressbar { top: 0px; }
}
@media screen and (max-height: 700px) and (min-height: 601px) {
  .imagepane div img { height: 400px; }
  .progressbar { top: 0px; }
}
@media screen and (max-height: 600px) and (min-height: 401px) {
  .imagepane div img { height: 333px; }
  .progressbar { top: 0px; }
}
@media screen and (max-height: 500px) and (min-width: 640px) {
  .imagepane div img { height: 270px; }
  .progressbar { margin: 0.5em 0 0 !important; }
  p.undecided { margin-top: -2.7em; position: relative; }
}
@media screen and (max-height: 400px) {
  .imagepane div img { height: 180px; }
  .progressbar { top: 7px; }
  p.undecided { margin-top: -2.7em; position: relative; }
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
    button:first-child { margin-right: 10px; }
  }
}

.lead {
  padding: 0.5em;
}

.vs-button.vote {
  font-weight: bold;
  width: 5em;
  width: 50%;
  border-radius: 0px;
  color: black;
  text-shadow: 1px 1px 1px white;
}
.vs-button.vote:first-child {
  border-right: 1px solid white;
}

.vote-count {
  display: none; /* Ignore for now */
  margin-top: 1em;
  color: #999;
}

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
