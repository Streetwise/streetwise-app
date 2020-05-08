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
        <vs-select v-model="selectedIssue">
          <vs-select-item :key="index" :value="item.v" :text="item.t" v-for="(item,index) in issueList" />
        </vs-select>
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
        { v: 'left', t: 'das linke Bild ist unklar' },
        { v: 'right', t: 'das rechte Bild ist unklar' },
        { v: 'both', t: 'beide Bilder sind unklar' },
        { v: 'same', t: 'beide Bilder sind zu ähnlich' }
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
</style>
