<template lang="pug">
.complete
  .survey(v-show='!surveyComplete')
    h1 Fast geschafft!
    p.lead
      | Erz&auml;hl uns kurz von dir.
    a(@click='showBlockquote=true', href='#')
      span.material-icons.info-button
        | info
      | Deine Angaben werden nicht an Dritte weitergegeben und von uns ausschliesslich f&uuml;r die anonyme Auswertung dieser Umfrage genutzt.

    blockquote(v-show='showBlockquote')
      | Deine Angaben helfen uns, belastbare Aussagen &uuml;ber die Beteiligung der Umfrage machen zu k&ouml;nnen.
      | So ist es beispielweise wichtig f&uuml;r uns zu wissen, wie spezifische Altersgruppen r&auml;umliche Situationen einsch&auml;tzen.

    form
      vs-row(vs-w='12')
        vs-col(vs-type='flex', vs-w='4')
          | Ich bin:
        vs-col(vs-type='flex', vs-w='8')
          select(v-model='surveyAge', v-bind:class='{ active: surveyAge }')
            option(:key='index', :value='item.value', v-for='(item, index) in listAges') {{ item.text }}
      vs-row(vs-w='12', style='margin-top:1em')
        vs-col(vs-type='flex', vs-w='4')
          | Geschlecht:
        vs-col(vs-type='flex', vs-w='8')
          select(v-model='surveyGender', v-bind:class='{ active: surveyGender }')
            option(:key='index', :value='item.value', v-for='(item, index) in listGenders') {{ item.text }}
      vs-row(vs-w='12', style='margin-top:1em')
        vs-col(vs-type='flex', vs-w='4')
          | Wohnort (Kanton):
        vs-col(vs-type='flex', vs-w='8')
          select(v-model='surveyCanton', v-bind:class='{ active: surveyCanton }')
            option(:key='index', :value='item.c', v-for='(item, index) in listCantons') {{ item.n }}

      center
        vs-button(flat='', size='large', color='success', style='margin: 1em 0', @click='submitForm') abschliessen

  div.survey-contest(v-show='surveyComplete && surveyRaffle')
    center.thanks
      | Herzlichen Dank f&uuml;r deine Teilnahme!
    iframe(src='https://docs.google.com/forms/d/e/1FAIpQLSck2tNAqXEOXwCeIdzKW5PrSEEw-yAnN0MVzwQGlAZ5Ysg6YQ/viewform?embedded=true', width='100%', height='500', frameborder='0', marginheight='0', marginwidth='0') Loading&mldr;
    center.survey-next
      //- a(href='https://forms.gle/SoFeC5tRiJdiEvoU6', target='_blank')
      //-   vs-button(flat='', type='line', color='light') Formular im Vollbildmodus anzeigen
      vs-button(flat='', size='large', color='success', @click='nextSubscribe') weiter

  div.survey-feedback(v-show='surveyComplete && !surveyRaffle')
    .thanks(@click='scrollToSubmit')
      | Hast du auf&#32;
      b Senden
      | &#32;geklickt? Wenn nicht, tippe hier.
    iframe(src='https://docs.google.com/forms/d/e/1FAIpQLSe95u0jGrf04V44J75dbuI5y3RbpiL00eqyw84B8v_rH9HrPw/viewform?embedded=true', width='100%', height='500', frameborder='0', marginheight='0', marginwidth='0') Loading&mldr;
    center.survey-next
      //- a(href='https://forms.gle/fDcXHYkSire7GRiU9', target='_blank')
      //-   vs-button(flat='', size='large', type='line', color='light') Formular im Vollbildmodus anzeigen
      span.together
        vs-button(flat='', size='large', color='primary', type='border', @click='backSubscribe') zurück
        vs-button(flat='', size='large', color='success', @click='skipSubscribe') fertig
</template>

<script>
import $backend from '../backend'
export default {
  name: 'Complete',
  components: {
  },
  props: {
    responses: 0,
    campaign: {
      type: Number,
      default: 1
    },
    skipsurvey: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      responsesRequired: 10,
      // Form state
      showBlockquote: false,
      surveyComplete: this.skipsurvey,
      surveyRaffle: true,
      // Survey data
      surveyAge: null,
      surveyGender: null,
      surveyCanton: null,
      // Survey values
      listAges: [
        { text: '12 oder jünger', value: 1 },
        { text: 'zwischen 13 und 19', value: 13 },
        { text: 'zwischen 20 und 39', value: 20 },
        { text: 'zwischen 40 und 64', value: 40 },
        { text: 'zwischen 65 und 79', value: 65 },
        { text: '80 oder älter', value: 80 },
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
        return this.$vs.notify({ text: 'Bitte überprüfe deine Angaben', color: 'warning', position: 'top-center' })
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
            return this.$vs.notify({ text: 'Da ist etwas schiefgegangen. Bitte wiederhole deine Eingabe.', color: 'warning', position: 'top-center' })
          }
          // this.$vs.notify({ text: 'Gespeichert', color: 'success' })
          this.surveyComplete = true
          window.scrollTo(0, 0)
          // Continue to 2nd round of wiser
          this.$router.push({ name: 'wise', params: { didsurvey: true } })
        }).catch(error => {
          console.warn(error.message)
          this.$vs.notify({ text: 'Es gab einen Fehler', color: 'danger', position: 'top-center' })
        })
    },
    scrollToSubmit: function () {
      this.backSubscribe()
      window.scrollTo(0, 100000)
    },
    backSubscribe: function () {
      this.surveyRaffle = true
    },
    nextSubscribe: function () {
      this.surveyRaffle = false
      window.scrollTo(0, 0)
    },
    skipSubscribe: function () {
      this.$router.push({ name: 'finish' })
    }
  },
  mounted () {
    if (this.responses < this.responsesRequired) {
      // This should not happen.
      console.warn('Too few responses', this.responses)
      // if (!window.prompt('Du hast weniger als ' + this.responsesRequired + ' beantwortet. Trotzdem weiterfahren?')) {
      //   this.$router.push({ name: 'wise' })
      // }
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
    position: fixed;
    bottom: 0px; left: 0px;
    padding-bottom: 3px;
    width: 100%;
    text-align: center;
    z-index: 1000;
    background: white;

    button { margin-right: 1em; }
  }

  .survey-feedback .thanks {
    b {
      border-radius: 5px;
      background: rgb(224, 69, 0);
      padding: 5px;
      color: white;
    }
    opacity: 0.8;
    cursor: pointer;
  }
}
@media screen and (min-height: 801px) {
  iframe { height: 900px; }
}
@media screen and (max-height: 800px) and (min-height: 601px) {
  iframe { height: 600px; }
}
@media screen and (max-height: 600px) and (min-height: 401px) {
  iframe { height: 800px; }
}
@media screen and (max-height: 500px) and (min-width: 750px) {
  iframe { height: 1100px; }
  .survey-feedback iframe { height: 1600px; }
}
@media screen and (max-height: 500px) and (max-width: 749px) {
  .complete { margin: 1em; }
  iframe { height: 900px; }
  .survey-feedback iframe { height: 2000px; }
}
@media screen and (max-width: 600px) {
  .complete {
    margin: 1em;
  }
  iframe { height: 1400px; }
  .survey-feedback iframe { height: 2500px; }
}
</style>
