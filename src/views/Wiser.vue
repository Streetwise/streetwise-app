<template>
  <div class="wiser">
    <ImageVote
      msg="Welche Situation sieht sicherer aus?"
    />
    <vs-popup fullscreen title="Anleitung" :active.sync="popupActive">
      <div class="content centerx">
        <h1>Jetzt bist du dran!</h1>
        <p>
          Wir zeigen dir Bildpaare und du schätzt ein, in welcher Umgebung du dich sicherer fühlen würdest.
        </p>
        <i>Zum Beispiel:</i>
        <div><img src="@/assets/example.jpg"></div>
        <p>
          <b>Links</b> bsw. <b>Rechts</b> tippen wenn das Bild auf die entsprechende Seite eine sicherere Gefühl entspricht. Wenn es zu schwierig ist, die Bilder zu unterscheiden, tippe auf <b>Unsicher</b>. Bitte beantworte alle 10 Bildpaare.
        </p>
        <center>
          <vs-button flat size="large" color="success" @click="popupActive=false">Los geht's !</vs-button>
        </center>
      </div>
    </vs-popup>
  </div>
</template>

<script>
import ImageVote from '@/components/ImageVote.vue'

export default {
  name: 'wiser',
  components: {
    ImageVote
  },
  data () {
    return {
      popupActive: true
    }
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
</style>
