<template>
  <div class="complete">
    <div class="survey" v-show="!surveyComplete">
      <h1>Letzte Schritte</h1>
      <p class="lead">
        Erzähl uns kurz von dir.
      </p>
      <a @click="showBlockquote=true" href="#">
        <span class="material-icons info-button">
        info
        </span>
        Wir nutzen deine Angaben ausschliesslich für die anonyme Auswertung dieser Umfrage.
      </a>
      <blockquote v-show="showBlockquote">
        Deine Angaben helfen uns, belastbare Aussagen über die Beteiligung der Umfrage machen zu können.
        So ist es beispielweise wichtig für uns zu wissen, welche Altersgruppe räumliche Situationen wie einschätzt.
      </blockquote>
      <form style="margin-top:3em">
        <vs-row vs-w="12">
          <vs-col vs-type="flex" vs-w="12">
            <b>Ich&nbsp;bin:&nbsp;</b><select
              label="Ich bin:"
              >
              <option :key="index" :value="item.value" v-for="(item, index) in listAges">{{ item.text }}</option>
            </select>
          </vs-col>
        </vs-row>
        <vs-row vs-w="12" style="margin-top:1em">
          <vs-col vs-type="flex" vs-w="12">
            <b>&nbsp;Ich&nbsp;bin:&nbsp;</b><select
              label="Ich bin:"
              >
              <option :key="index" :value="item.value" v-for="(item, index) in listGenders">{{ item.text }}</option>
            </select>
          </vs-col>
        </vs-row>

        <vs-button flat size="large" color="success"
          style="margin: 1em 0"
          @click="submitForm">Abschliessen</vs-button>
      </form>
    </div>
    <div class="raffle" v-show="surveyComplete">
      <h1>Herzlichen Dank für deine Teilnahme</h1>

      <p>Du kannst wenn gewünscht hier für unser Wettbewerb und zum unsere Newsletter anmelden, und dann weitere Bilder beurteilen.</p>

      <vs-checkbox v-model="confirmRaffle">
        Ich will ein iPhone gewinnen!
        Bitte <a href="https://streetwise.space/disclaimer" target="_blank">Wettbewerbsbedingungen</a> anschauen.
      </vs-checkbox>

      <vs-checkbox v-model="confirmSubscribe">
        Ich will über die Ergebnisse dieser Umfrage informiert werden.
      </vs-checkbox>

      <center>
        <vs-input
          class="input-email"
          :success="emailValid"
          success-text="The address looks valid"
          placeholder="E-mail"
          v-model="emailAddress"
          @change="checkEmail" />
        <vs-button flat size="large" color="primary" @click="submitSubscribe">Senden</vs-button>
        &nbsp;
        <vs-button flat size="large" color="grey" @click="skipSubscribe">Überspringen</vs-button>
      </center>

      <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSe95u0jGrf04V44J75dbuI5y3RbpiL00eqyw84B8v_rH9HrPw/viewform?embedded=true" width="100%" height="1654" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
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
      showBlockquote: false,
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
      window.scrollTo(0, 0)
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
      let disableSignup = true
      if (disableSignup) {
        this.$vs.dialog({
          type: 'alert',
          color: 'success',
          title: 'Hinweis',
          text: 'Es ist noch nicht möglich, sich am Wettbewerb zu beteiligen oder zu abonnieren. Aber es geht gleich los!'
        })
        this.$vs.notify({ text: 'Gespeichert', color: 'success' })
        return
      }
      this.skipSubscribe()
    },
    skipSubscribe: function () {
      this.$router.push({ name: 'wise', params: { skipintro: true } })
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

  .vs-row, .vs-col { margin: 0; }

  .info-button {
    color: blue;
    float: left;
    display: inline-block;
    margin-right: 0.5em;
    font-size: 200%;
  }

  .input-email {
    display: inline-block;
    margin-right: 1em;
    transform: scale(1.4);
  }
}
</style>
