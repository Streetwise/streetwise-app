<template>
  <div class="social-icons">
    <a :href="linkTwitter" target="_blank" title="Tweet about this">
      <twitter-icon />
      <span v-if="expand">Twitter</span>
    </a>
    <a :href="linkFacebook" target="_blank" title="Like on Facebook">
      <facebook-icon />
      <span v-if="expand">Facebook</span>
    </a>
    <a :href="linkLinkedin" target="_blank" title="Post on LinkedIn">
      <linkedin-icon />
      <span v-if="expand">LinkedIn</span>
    </a>
    <a :href="linkInstagram" target="_blank" title="Share on Instagram">
      <instagram-icon />
      <span v-if="expand">Instagram</span>
    </a>
  </div>
</template>

<script>
import { TwitterIcon, FacebookIcon, LinkedinIcon, InstagramIcon } from 'vue-feather-icons'

export default {
  components: {
    TwitterIcon, FacebookIcon, LinkedinIcon, InstagramIcon
  },
  data () {
    return {
      linkTwitter: 'https://twitter.com/intent/tweet?hashtags=streetwisespace&text=&url=https%3A%2F%2Fstreetwise.space',
      linkFacebook: 'https://www.facebook.com/streetwise.space/',
      linkLinkedin: 'https://www.linkedin.com/feed/update/urn:li:activity:6665512171503448064/',
      linkInstagram: 'https://www.instagram.com/explore/tags/streetwisespace/'
    }
  },
  props: {
    color: {
      type: String,
      default: 'darkgreen'
    },
    expand: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="scss" scoped>
a {
  background: none;
  border: 0;
  padding: 10px;
  // transition: color .15s ease-in-out;
  width: 48px;
  height: 48px;
  position: relative;
  vertical-align: middle;
  span { margin-left: 1em; }
}

.theme-enter-active, .theme-leave-active {
  transition: transform .25s ease-in-out, opacity .25s ease-in-out;
}
.theme-enter, .theme-leave-to /* .fade-leave-active below version 2.1.8 */ {
  transform: translateY(20px) scale(.5);
  opacity: 0;
}
</style>
