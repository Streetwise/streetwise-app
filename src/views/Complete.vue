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
          <vs-col vs-type="flex" vs-w="4">
            Ich bin:
          </vs-col>
          <vs-col vs-type="flex" vs-w="8">
            <select v-model="surveyAge"
              v-bind:class="{ active: surveyAge }">
              <option :key="index" :value="item.value" v-for="(item, index) in listAges">{{ item.text }}</option>
            </select>
          </vs-col>
        </vs-row>
        <vs-row vs-w="12" style="margin-top:1em">
          <vs-col vs-type="flex" vs-w="4">
            Geschlecht:
          </vs-col>
          <vs-col vs-type="flex" vs-w="8">
            <select v-model="surveyGender"
              v-bind:class="{ active: surveyGender }">
              <option :key="index" :value="item.value" v-for="(item, index) in listGenders">{{ item.text }}</option>
            </select>
          </vs-col>
        </vs-row>
        <vs-row vs-w="12" style="margin-top:1em">
          <vs-col vs-type="flex" vs-w="4">
            In Kanton:
          </vs-col>
          <vs-col vs-type="flex" vs-w="8">
            <select v-model="surveyCanton"
              v-bind:class="{ active: surveyCanton }">
              <option :key="index" :value="item.c" v-for="(item, index) in listCantons">{{ item.n }}</option>
            </select>
          </vs-col>
        </vs-row>

        <vs-button flat size="large" color="success"
          style="margin: 1em 0"
          @click="submitForm">Abschliessen</vs-button>
      </form>
    </div>

    <div class="raffle" v-show="surveyComplete">
      <h1>Herzlichen Dank für die Teilnahme</h1>

      <img class="icon right" src="@/assets/icons/nature.svg">
      <p>Du kannst dich hier für die Verlosung anmelden und, wenn du magst, dann weitere Bilder beurteilen.</p>

    </div>
    <iframe v-show="surveyComplete"
      src="https://docs.google.com/forms/d/e/1FAIpQLSck2tNAqXEOXwCeIdzKW5PrSEEw-yAnN0MVzwQGlAZ5Ysg6YQ/viewform?embedded=true" width="100%" height="500" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
    <center v-show="surveyComplete" class="survey-next">
      <a href="https://forms.gle/SoFeC5tRiJdiEvoU6" target="_blank">
        <vs-button flat size="large" color="black">Vollbild</vs-button>
      </a>
      <vs-button flat size="large" color="success" @click="skipSubscribe">Weiter beurteilen</vs-button>
    </center>
  </div>
</template>

<script>
import $backend from '../backend'
export default {
  name: 'Complete',
  components: {
  },
  data () {
    return {
      // Form state
      showBlockquote: false,
      surveyComplete: false,
      // Survey data
      surveyAge: null,
      surveyGender: null,
      surveyCanton: null,
      // Survey values
      listAges: [
        { text: '19 oder jünger', value: 1 },
        { text: 'zwischen 20 und 39', value: 2 },
        { text: 'zwischen 40 und 64', value: 3 },
        { text: '65 oder älter', value: 4 },
        { text: '(ich möchte keine Angaben machen)', value: -1 }
      ],
      listGenders: [
        { text: 'weiblich', value: 1 },
        { text: 'männlich', value: 2 },
        { text: 'andere', value: 3 },
        { text: '(ich möchte keine Angaben machen)', value: -1 }
      ],
      // eslint-disable-next-line
      listCantons: [{n:"(nicht in der Schweiz)",c:"XX"}, {n:"Aargau",c:"AG"}, {n:"Appenzell Ausserrhoden",c:"AR"}, {n:"Appenzell Innerrhoden",c:"AI"}, {n:"Basel-Landschaft",c:"BL"}, {n:"Basel-Stadt",c:"BS"}, {n:"Bern",c:"BE"}, {n:"Freiburg",c:"FR"}, {n:"Genf",c:"GE"}, {n:"Glarus",c:"GL"}, {n:"Graubünden",c:"GR"}, {n:"Jura",c:"JU"}, {n:"Luzern",c:"LU"}, {n:"Neuenburg",c:"NE"}, {n:"Nidwalden",c:"NW"}, {n:"Obwalden",c:"OW"}, {n:"Schaffhausen",c:"SH"}, {n:"Schwyz",c:"SZ"}, {n:"Solothurn",c:"SO"}, {n:"St. Gallen",c:"SG"}, {n:"Tessin",c:"TI"}, {n:"Thurgau",c:"TG"}, {n:"Uri",c:"UR"}, {n:"Waadt",c:"VD"}, {n:"Wallis",c:"VS"}, {n:"Zug",c:"ZG"}, {n:"Zürich",c:"ZH"}, {n:"(ich möchte keine Angaben machen)",c:"00"}]
      // src: https://query.wikidata.org/sparql?query=%23Cantons%0ASELECT%20%3Fitem%20%3Fn%20%3FitemCode%0AWHERE%20%0A%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ23058.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP395%20%3FitemCode.%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22de%22.%20%7D%0A%7D
    }
  },
  methods: {
    submitForm: function () {
      if (this.surveyAge === null ||
          this.surveyGender === null ||
          this.surveyCanton === null) {
        return this.$vs.notify({ text: 'Bitte überprüfen Sie ihre Angaben', color: 'warning', position: 'top-center' })
      }
      $backend.saveSurvey(
        {
          age: this.surveyAge,
          gen: this.surveyGender,
          can: this.surveyCanton
        }
      )
        .then(responseData => {
          if (responseData === null) {
            return this.$vs.notify({ text: 'Bitte nochmal wiederholen', color: 'warning', position: 'top-center' })
          }
          this.$vs.notify({ text: 'Gespeichert', color: 'success' })
          this.surveyComplete = true
          window.scrollTo(0, 0)
        }).catch(error => {
          console.warn(error.message)
          this.$vs.notify({ text: 'Es gab einen Fehler', color: 'danger', position: 'top-center' })
        })
    },
    skipSubscribe: function () {
      this.$router.push({ name: 'wise', params: { skipintro: true } })
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

  form select {
    font-size: 140%;
    border: 2px solid blue;
    width: 100%;

    &.active {
      border-color: lightgreen;
      background: white;
    }
  }

  img.icon {
    width: 50px; margin-top: 1em;
    &.left { float:left; margin-right: 1em; }
    &.right { float:right; margin-left: 2em;  }
  }

  .info-button {
    color: blue;
    float: left;
    display: inline-block;
    margin-right: 0.5em;
    font-size: 200%;
  }

  .input-email {
    display: inline-block;
    margin-right: 2em;
    transform: scale(1.3);
    margin-top: 5px;
    vertical-align: top;
  }

  .survey-next {
    margin-top: 1em;
    button { margin-right: 1em; }
  }
}

@media screen and (max-width: 600px) {
  .complete {
    margin: 1em;
  }
  iframe {
    width: 100%;
    height: 330px;
    margin: 0px;
    padding: 0px;
  }
}
</style>
