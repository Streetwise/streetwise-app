<template>
  <div class="progress-goals">
    <vs-progress :height="40" :percent="votePercent" color="success" />
    <div class="progress-text">
      <b class="count">{{voteCount}}</b>
      <small>&nbsp;von&nbsp;</small>
      <b class="goal">{{voteGoal.toLocaleString('de-CH')}}</b>
      <small>&nbsp;Bildbewertungen gesammelt</small>
    </div>
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
  margin: 2em 0 1.5em;
  .vs-progress--background {
    text-align: left;
  }
  .progress-text {
    margin-top: 0.3em;
    margin-bottom: 0.3em;
    small { color: #777; }
    // span, b.goal { font-size: 85% }
  }
}
</style>
