<template>
  <div class="imagevote">
    <div class="progressbar" v-on:click="showResourceList = !showResourceList">
      <p>{{ voteCount }} / {{ voteTotal }}</p>
      <vs-progress :height="12" :percent="votePercent" color="success"></vs-progress>
    </div>
    <div class="imagepane">
      <div class="left"  :style="{ backgroundImage: `url(${imageLeftUrl})`  }" />
      <div class="right" :style="{ backgroundImage: `url(${imageRightUrl})` }" />
    </div>

    <p>
      <vs-button flat size="large" @click.prevent="voteLeft">Left</vs-button>
      &nbsp;
      <vs-button flat size="large" @click.prevent="voteRight">Right</vs-button>
    </p>

    <p style="margin:1em">
      <vs-button type="border" @click.prevent="voteUndecided">Unsure</vs-button>
      &nbsp;
      <vs-button type="border" @click.prevent="voteSkip">Next</vs-button>
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
  name: 'about',
  data () {
    return {
      showResourceList: false,
      resources: [],
      error: '',
      imageLeft: 0,
      imageLeftUrl: '/loading.gif',
      imageRight: 0,
      imageRightUrl: '/loading.gif',
      timeStart: Date.now(),
      voteCount: 0,
      voteTotal: 5,
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
  div {
    display: inline-block;
    width: 40%;
    height: 60%;
    min-height: 400px;
    padding: 3px;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: bottom left;
  }
}

.vs-button.large {
  font-weight: bold;
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
