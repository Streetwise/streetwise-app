<template>
  <div class="progress-goals">
    <vs-progress :height="45" :percent="votePercent" color="success" />
    <div>{{voteCount}} von {{voteGoal.toLocaleString()}}</div>
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
  margin: 1.5em 0;
  height: 2em;

  & div {
    font-weight: bold;
    margin-top: -2.7em;
    margin-bottom: 0.7em;
  }
}
</style>
