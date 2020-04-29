<template>
  <div class="wiser">
    <ImageVote
      msg="Welche Situation sieht sicherer aus?"
      :skipintro="skipintro"
    />
    <vs-popup fullscreen title="Jetzt bist du dran ..." :active.sync="popupActive">
      <div class="content centerx">
        <p>
          Wir zeigen dir Bildpaare und du schätzt ein, in welcher Umgebung du dich sicherer fühlen würdest. Drücke entsprechend auf <b>Links</b> bzw. <b>Rechts</b>.
        </p>
        <div><img style="max-width:100%" src="@/assets/example.jpg"></div>
        <p style="font-size:80%">
          Zu schwierig zu entscheiden? Wähle <b>Unsicher</b>. Tippe auf ein Bild, um es in <b>Vollbild</b> anzuschauen. Bitte beantworte <b>mindestens</b> 10 Bildpaare.
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
    this.popupActive = !this.skipintro
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
@media screen and (max-width: 600px) {
  .centerx { margin: 1em; }
}
</style>
