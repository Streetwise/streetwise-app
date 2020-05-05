<template>
  <div class="imagevote">
    <div class="progressbar" v-on:click="showResourceList = !showResourceList">
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
      ></div>
    </vs-popup>

    <p>
      <vs-button type="border" size="small" color="warning" class="complain left" @click.prevent="complainLeft">🚩</vs-button>

      <vs-button flat size="large" color="success" class="vote left" @click.prevent="voteLeft">Links</vs-button>

      <vs-button type="border" class="undecided" @click.prevent="voteUndecided">Unsicher</vs-button>

      <vs-button flat size="large" color="success" class="vote right" @click.prevent="voteRight">Rechts</vs-button>

      <vs-button type="border" size="small" color="warning" class="complain right" @click.prevent="complainRight">🚩</vs-button>
    </p>

    <p style="margin:1em">
      <vs-button type="line" color="rgb(200,200,200)" @click.prevent="voteSkip">Überspringen</vs-button>
    </p>

    <p style="color:red">{{ error }}</p>

    <p v-show="showResourceList" v-for="r in resources" :key="r.id">
      <span v-if="r.is_undecided">
        Undecided |
      </span>
      <span v-if="!r.is_undecided">
        Choice: {{r.choice_id}} |
      </span>
      Time: {{r.time_elapsed}} |
      At: {{r.created | formatTimestamp }}
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
      resources: [],
      showResourceList: false,
      error: '',
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
              voter.$router.push('complete')
            }
          })
        } else {
          this.$router.push('complete')
        }
      }
      return false
    },
    nextImagePair (skip = false) {
      this.error = ''
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
    castVote (isRight) {
      $backend.castVote(
        isRight,
        this.imageLeft,
        this.imageRight,
        this.elapsedTime()
      )
        .then(responseData => {
          if (responseData !== null) {
            this.resources.push(responseData)
            this.nextImagePair()
          }
        }).catch(error => {
          console.warn(error.message)
          if (error.message.indexOf('429')) {
            this.error = 'Please slow down'
          } else {
            this.error = 'There was an error, please try again'
          }
        })
    },
    voteLeft () {
      this.castVote(false)
    },
    voteRight () {
      this.castVote(true)
    },
    voteUndecided () {
      let voter = this
      this.$vs.dialog({
        type: 'confirm',
        color: 'warning',
        title: `Bestätigen`,
        text: 'Bist du sicher, dass du der mehr sichere der beiden Situationen *nicht* entscheiden kannst?',
        accept: function () {
          voter.castVote(null)
        }
      })
    },
    voteSkip () {
      this.nextImagePair(true)
      this.$vs.notify({ text: 'Übersprungen!', color: 'warning' })
    },
    complainImage (isRight) {
      let voter = this
      let welchen = isRight ? 'rechten' : 'linken'
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: `Problem melden`,
        text: 'Falls du den ' + welchen + ' Bild nicht gut sehen kannst oder eine andere Problem melden willst, bitte im folgende Dialog kurz beschreiben.',
        accept: function () {
          let note = prompt('Problem beschreiben:')
          if (note) {
            // TODO: needs API !
            voter.$vs.notify({ text: 'Danke fürs melden!', color: 'warning' })
          }
        }
      })
    },
    complainLeft () {
      this.complainImage(false)
    },
    complainRight () {
      this.complainImage(true)
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
  .lead {
    font-size: 90%;
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
}

.lead { margin: 1em; }

.vs-button.vote {
  font-weight: bold;
  width: 5em;
}

.undecided {
  margin: 0.5em;
  opacity: 0.8;
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
