<template>
  <div class="issuebox">
    <vs-prompt
      @accept="accept"
      @cancel="close"
      @close="close"
      :active="active"
      acceptText="Bestätigen"
      cancelText="Zurück"
      title="Unentschieden"
      >
      <div class="body">
        <p>Kannst du dich bei diesem Bildpaar wirklich nicht entscheiden, wo du dich sicherer fühlen würdest?</p>
        <select size="large" v-model="selectedIssue">
          <option
            :key="index" :value="item.v"
            v-for="(item,index) in issueList">
            {{ item.t }}
          </option>
        </select>
      </div>
     </vs-prompt>
  </div>
</template>

<script>
export default {
  name: 'IssueBox',
  props: {
    active: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      selectedIssue: '',
      issueList: [
        { v: 'left', t: 'Das linke Bild ist unklar / schwierig zu beurteilen' },
        { v: 'right', t: 'Das rechte Bild ist unklar / schwierig zu beurteilen' },
        { v: 'both', t: 'Beide Bilder sind unklar / schwierig zu beurteilen' },
        { v: 'same', t: 'Die zwei Bilder sind zu ähnlich' }
      ]
    }
  },
  methods: {
    accept () {
      this.$emit('close-box', this.selectedIssue)
    },
    close () {
      this.selectedIssue = null
      this.$emit('close-box', false)
    }
  }
}
</script>

<style scoped lang="scss">
p {
  font-family: 'OpenSans', Helvetica, Arial, sans-serif;
  font-size: 120%;
  margin-bottom: 1em;
}

select {
  width: 100%;
  font-size: 125%;
}
</style>
