<template>
  <div class="crowd-source-goals-div">
    <div class="crowd-source-actual">{{voteCount}} total gesammelte Bilelbewertungen</div>
    <div class="crowd-source-target">tiel: 50,000 klicks</div>
  </div>
</template>

<script>
import $backend from '@/backend'
export default {
  name: 'CrowdSourceGoals',
  data: function () {
    return { voteCount: 0 }
  },

  beforeCreate: function () {
    $backend.getVoteCount()
      .then((res) => {
        this.voteCount = res.total_count
      })
  }
}
</script>

<style scoped lang="scss">
.crowd-source-goals-div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 8px;
}

.crowd-source-actual {
  width: 50%;
  padding: 8px;
  border: solid black 1px;
  border-radius: 8px;
}

.crowd-source-target {
  float: right;
  padding: 8px;
}

@media all and (max-height: 600px) {
  .crowd-source-actual {
    width: 40%
  }
}
@media screen and (max-width: 600px) {
  .crowd-source-actual {
    width: 70%
  }
}
</style>
