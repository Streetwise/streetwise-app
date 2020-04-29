<template>
  <div class="complete">
    <div class="survey" v-show="!surveyComplete">
      <h1>Letzte Schritte</h1>
      <p class="lead">
        Erzähl uns kurz von dir.
      </p>
      <p>
        Wir nutzen deine Angaben ausschliesslich für die anonyme Auswertung dieser Umfrage.
      </p>
      <blockquote>
        Deine Angaben helfen uns, belastbare Aussagen über die Beteiligung der Umfrage machen zu können.
        So ist es beispielweise wichtig für uns zu wissen, welche Altersgruppe räumliche Situationen wie einschätzt.
      </blockquote>
      <form>
        <vs-row vs-w="12">
          <vs-col vs-type="flex" vs-w="6">
            <b>Ich bin:</b>
            <select
              label="Ich bin:"
              >
              <option :key="index" :value="item.value" v-for="(item, index) in listAges">{{ item.text }}</option>
            </select>
          </vs-col>
        </vs-row><vs-row vs-w="12">
          <vs-col vs-type="flex" vs-w="6">
            <b>Ich bin:</b>
            <select
              label="Ich bin:"
              >
              <option :key="index" :value="item.value" v-for="(item, index) in listGenders">{{ item.text }}</option>
            </select>
          </vs-col>
        </vs-row>

        <vs-button flat size="large" color="success" @click="submitForm">Weiter</vs-button>
      </form>
    </div>
    <div class="raffle" v-show="surveyComplete">
      <h1>Herzlichen Dank für deine Teilnahme</h1>

      <vs-checkbox v-model="confirmRaffle">
        Ich will ein iPhone gewinnen!
        Bitte <a href="https://streetwise.space/disclaimer" target="_blank">Wettbewerbsbedingungen</a> anschauen.
      </vs-checkbox>

      <vs-checkbox v-model="confirmSubscribe">
        Ich will über die Ergebnisse dieser Umfrage informiert werden.
      </vs-checkbox>

      <center>
        <vs-input
          :success="emailValid"
          success-text="The address looks valid"
          placeholder="E-mail"
          v-model="emailAddress"
          @change="checkEmail" />

        <vs-button flat size="large" color="primary" @click="submitSubscribe">Senden</vs-button>
      </center>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Complete',
  components: {
  },
  data () {
    return {
      surveyComplete: false,
      confirmRaffle: true,
      confirmSubscribe: true,
      emailAddress: '',
      emailValid: false,
      listAges: [
        { text: '19 oder jünger', value: 0 },
        { text: 'zwischen 20 und 39', value: 0 },
        { text: 'zwischen 40 und 64', value: 0 },
        { text: '65 oder älter', value: 0 },
        { text: 'ich möchte keine Angaben machen', value: 0 }
      ],
      listGenders: [
        { text: 'weiblich', value: 0 },
        { text: 'männlich', value: 0 },
        { text: 'andere', value: 0 },
        { text: 'ich möchte keine Angaben machen', value: 0 }
      ]
    }
  },
  methods: {
    submitForm: function () {
      this.$vs.notify({ text: 'Gespeichert', color: 'success' })
      this.surveyComplete = true
    },
    submitSubscribe: function () {
      if (!this.emailValid) {
        this.$vs.dialog({
          type: 'alert',
          color: 'warning',
          title: 'Hinweis',
          text: 'Bitte alle Angaben überprüfen.'
        })
        return
      }
      this.$vs.notify({ text: 'Gespeichert', color: 'success' })
      this.$router.push('/')
    },
    checkEmail: function () {
      this.emailValid = this.emailAddress.length - 2 > this.emailAddress.lastIndexOf('.') && this.emailAddress.lastIndexOf('.') > this.emailAddress.indexOf('@') > 0
    }
  }
}
</script>

<style lang="scss" scoped>
.complete {
  margin: 2em 15%;

  p, div, blockquote, form {
    margin: 1em 0;
    text-align: left;
  }

  h1 { font-size: 200%; }
  .lead { font-size: 125%; }

  .vs-button { margin: 1em 0; }
  .vs-row, .vs-col { margin: 0; }
}
</style>
