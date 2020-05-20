<template>
  <div class="progress-goals">
    <vs-progress :height="45" :percent="votePercent" color="success" />
    <div><b class="count">{{voteCount}}</b>
      <span>&nbsp;von&nbsp;</span>
      <b class="goal">{{voteGoal.toLocaleString('de-CH')}}</b></div>
    <small>Bildbewertungen gesammelt</small>
  </div>
</template>

<script>
import $backend from '@/backend'
export default {
  name: 'ProgressGoals',
  data () {
    return {
      voteCount: 0,
      votePercent: 0,
      voteGoal: 50000
    }
  },

  beforeCreate: function () {
    $backend.getVoteCount()
      .then((res) => {
        this.voteCount = res.total_count
        this.votePercent = 100 * this.voteCount / this.voteGoal
      })
  }
}
</script>

<style scoped lang="scss">
.progress-goals {
  clear: both;
  width: 100%;
  margin: 3em 0 1.5em;
  height: 2em;

  & div {
    margin-top: -2.7em;
    margin-bottom: 0.7em;
    span, b.goal {
      font-size: 85%
    }
  }
}
</style>
