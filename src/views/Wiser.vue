<template>
  <div class="wiser">
    <p class="lead">Choose the image that feels safer.</p>

    <img src="@/assets/test/24625645967_f9e6f81566_k.jpg">
    <img src="@/assets/test/mesch - Helvetiagaertli.jpg">

    <p>
      <button href="" @click.prevent="fetchResource">Left</button>
      <button href="" @click.prevent="fetchResource">Right</button>
    </p>
    <button href="" @click.prevent="fetchResource">Unsure</button>

    <p v-for="r in resources" :key="r.timestamp">
      Server Timestamp: {{r.timestamp | formatTimestamp }}
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
      error: ''
    }
  },
  methods: {
    fetchResource () {
      $backend.fetchResource()
        .then(responseData => {
          this.resources.push(responseData)
        }).catch(error => {
          this.error = error.message
        })
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
