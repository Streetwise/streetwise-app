<template>
  <div class="imagevote">
    <div class="progressbar" v-on:click="showResourceList = !showResourceList">
      <p>{{ voteCount }} / {{ voteTotal }}</p>
      <vs-progress :height="12" :percent="votePercent" color="warning"></vs-progress>
    </div>

    <h4 class="lead">{{ msg }}</h4>

    <div class="imagepane">
      <div class="left"  :style="{ backgroundImage: `url(${imageLeftUrl})`  }" />
      <div class="right" :style="{ backgroundImage: `url(${imageRightUrl})` }" />
    </div>

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
    msg: String
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
      votePercent: 0
    }
  },
  methods: {
    elapsedTime () {
      return Math.round((Date.now() - this.timeStart) / 1000)
    },
    checkVotesComplete () {
      if (this.voteCount === this.voteTotal) {
        this.$vs.dialog({
          title: `Erledigt! Vielen Dank`,
          text: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
          cancel: function () { location.href = '/' },
          accept: function () { location.href = '/' }
        })
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
      console.log('Fetching image pair')
      $backend.getRandomImages()
        .then(responseData => {
          console.log(responseData)
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
          console.error(error.message)
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
      this.castVote(null)
    },
    voteSkip () {
      this.nextImagePair(true)
    },
    complainImage (isRight) {
      this.$vs.dialog({
        type: 'confirm',
        color: 'error',
        title: `Problem melden`,
        text: 'Falls du diesen Bild nicht gut sehen kannst oder eine andere Problem melden willst, bitte hier bestätigen.'
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
    min-height: 400px;
    padding: 3px;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: bottom left;
  }
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
