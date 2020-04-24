<template>
  <div class="wiser">
    <p class="lead">Choose the image that feels safer.</p>

    <img src="@/assets/test/24625645967_f9e6f81566_k.jpg">
    <img src="@/assets/test/mesch - Helvetiagaertli.jpg">

    <p>
      <button href="" @click.prevent="voteLeft">Left</button>
      <button href="" @click.prevent="voteRight">Right</button>
    </p>
    <button href="" @click.prevent="voteUndecided">Unsure</button>

    <p>{{resources.length}} votes</p>
    <p v-for="r in resources" :key="r.timestamp">
      <span v-if="r.is_undecided">
        Undecided |
      </span>
      <span v-if="!r.is_undecided">
        Choice: {{r.choice}} |
      </span>
      Time: {{r.timetaken}} |
      At: {{r.timestamp | formatTimestamp }}
    </p>
    <p>{{error}}</p>
  </div>
</template>

<script>

import $backend from '../backend'

export default {
  name: 'about',
  data () {
    return {
      resources: [],
      error: '',
      imageLeft: 'flickr',
      imageRight: 'mesch',
      timeStart: Date.now()
    }
  },
  methods: {
    elapsedTime () {
      return Math.round((Date.now() - this.timeStart) / 1000)
    },
    nextImagePair () {
      this.timeStart = Date.now()
    },
    castVote (isRight) {
      $backend.castVote(
        isRight,
        this.imageLeft,
        this.imageRight,
        this.elapsedTime()
      )
        .then(responseData => {
          this.resources.push(responseData)
          this.nextImagePair()
        }).catch(error => {
          this.error = error.message
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
    }
  }
}

</script>

<style lang="scss">
.wiser {
  text-align: center;
}

img { width: 40%; padding: 3px; }
</style>
