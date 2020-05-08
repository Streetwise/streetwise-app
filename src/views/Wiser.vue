<template>
  <div class="wiser">
    <ImageVote
      msg="Wo fühlst du dich sicherer?"
      :skipintro="skipintro"
    />
    <vs-popup title="Anleitungshilfe" :active.sync="popupActive">
      <div class="content centerx">
        <p>
          Wir zeigen dir Bildpaare und du schätzt ein, in welcher Umgebung du dich sicherer fühlen würdest.
          Stell dir vor, du betrachtest die Bilder aus der Perspektive als Fussgängerin, Skater, Trottinett- oder Velofahrer.
          Scrolle oder tippe auf ein Bild, um es zu vergrössern.
        </p>
        <center class="together">
          links 👈
          <vs-button disabled type="border" color="black" class="undecided">???</vs-button>
          👉 rechts
        </center>
        <!-- <div><img style="max-width:100%" src="@/assets/example.jpg"></div> -->
        <p>
          Klicke entsprechend auf links oder rechts für deine Auswahl. Kannst du dich nicht entscheiden? Dann wähle «Beide / Weiss nicht».
          Bitte beantworte <b>mindestens 10</b> Bildpaare.
        </p>
        <center>
          <vs-button flat size="large" color="success" @click="popupActive=false">Los geht's !</vs-button>
        </center>
      </div>
    </vs-popup>
    <center class="help-icon">
      <vs-button flat size="small" color="white" @click="popupActive=true" title="Anleitung">
        <vs-icon icon="help" size="small" bg="orange" round></vs-icon>
        <b>Anleitung</b>
      </vs-button>
    </center>
  </div>
</template>

<script>
import ImageVote from '@/components/ImageVote.vue'

export default {
  name: 'Wiser',
  components: {
    ImageVote
  },
  props: {
    skipintro: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      popupActive: false
    }
  },
  mounted () {
    // this.popupActive = !this.skipintro
  }
}
</script>

<style lang="scss" scoped>
.wiser {
  text-align: center;
  .lead {
    margin-top: 1em;
  }
}
.centerx {
  margin: 0 20%;
  font-size: 150%;
  p, div {
    margin: 1em 0;
  }
}
.together { white-space: nowrap; }
.help-icon {
  z-index: 10000;
  b { color: orange !important; font-size: 120%; }
  button { padding: 7px; }
}
.imagevote {
  margin-bottom: 7px;
}
@media screen and (max-height: 500px) {
  .help-icon {
    position: absolute;
    top: 0px; right: 0px;
    b { display: none; }
  }
}
@media screen and (max-width: 600px) {
  .centerx { margin: 1em; }
  .help-icon {
    position: absolute;
    top: 0px; left: 0px;
    b { display: none; }
  }
}
</style>
