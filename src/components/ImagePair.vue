<template>
  <div class="imagepane">
    <div class="left" @click="popupImage=true;popupLeft=true" ref="leftImagePane">
      <ImageContainer v-bind:source=this.leftImage />
    </div>
    <div class="right" @click="popupImage=true;popupLeft=false" ref="rightImagePane">
      <ImageContainer v-bind:source="this.rightImage" />
    </div>

    <vs-popup fullscreen
      classContent="lightbox-container" styleHeader="display:none"
      :active.sync="popupImage" @close="popupImage=false"
      :title="`${popupLeft ? 'Linkes Bild' : 'Rechtes Bild'}`">
      <div class="lightbox" @click="popupImage=false"
        :style="{ backgroundImage: `url(${popupLeft ? leftImage : rightImage})`  }"
      >
        <div class="buttons">
          <vs-button class="back-btn" flat size="large" color="black" type="border" @click="popupImage=false">Zurück</vs-button>
          <vs-button v-show="popupLeft" flat size="large" color="success" @click.prevent="voteLeft">Linkes Bild auswählen</vs-button>
          <vs-button v-show="!popupLeft" flat size="large" color="success" @click.prevent="voteRight">Rechtes Bild auswählen</vs-button>
        </div>
      </div>
    </vs-popup>
  </div>
</template>

<script>
import ImageContainer from '@/components/ImageContainer.vue'
export default {
  name: 'ImagePair',
  components: {
    ImageContainer
  },
  props: {
    leftImage: '',
    rightImage: '',
    voteLeft: Function,
    voteRight: Function
  },
  data: () => ({
    popupImage: false,
    popupLeft: false
  })
}
</script>

<style scoped lang=scss>
.lightbox {
  width: 100%; height: 100%;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center center;
  overflow: hidden;
  .buttons {
    position: absolute;
    bottom: 2em;
    width: 100%; margin-left: -30px;
    text-align: center;
    z-index: 1000;
    button:first-child { margin-right: 10px; }
    .back-btn { background-color: white; }
  }
}

.imagepane {
  text-align: center;
  width: 100%;
  overflow: hidden;
  div {
    display: inline-block;
    width: 50%;
    height: 60%;
    padding: 0px; margin: 0px;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
    overflow-y: hidden;
    overflow-x: scroll;
    img {
      padding: 0px; border: 0px; margin: 0px;
    }
  }
}

/* Vertical positioning of images */
@media screen and (min-height: 1200px) {
  .imagepane div img { height: 1000px; }
}
@media screen and (max-height: 1200px) and (min-height: 900px) {
  .imagepane div img { height: 660px; }
}
@media screen and (max-height: 900px) and (min-height: 700px) {
  .imagepane div img { height: 500px; }
}
@media screen and (max-height: 700px) and (min-height: 601px) {
  .imagepane div img { height: 400px; }
}
@media screen and (max-height: 600px) and (min-height: 401px) {
  .imagepane div img { height: 333px; }
}
@media screen and (max-height: 500px) and (min-width: 640px) {
  .imagepane div img { height: 260px;}
}
@media screen and (max-height: 400px) {
  .imagepane div img { height: 205px; }
}

</style>
