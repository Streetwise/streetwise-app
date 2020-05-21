import Vue from 'vue'
import Vuex from 'vuex'
import $backend from './backend'

Vue.use(Vuex)

const imageLoading = '/images/loading.gif'

const defaultImages = {
  left: { id: 0, url: imageLoading },
  right: { id: 0, url: imageLoading },
  invalid: false
}

export default new Vuex.Store({
  state: { images: defaultImages },

  mutations: {
    resetImages (state) { state.images = defaultImages },

    updateImages (state, payload) {
      state.images = {
        left: { id: payload[0].id, url: payload[0].Url },
        right: { id: payload[1].id, url: payload[1].Url },
        invalid: false
      }
    },

    invalidImages (state) {
      state.images.invalid = true
    }
  },
  actions: {
    async refreshImages (context) {
      try {
        const response = await $backend.getRandomImages()
        context.commit('updateImages', response)
      } catch (error) {
        console.warn(error.message)
        context.commit('resetImages')
      }
    },

    async imagePairInvalid (context) {
      if (!context.state.images.invalid) {
        context.commit('invalidImages')
      }
    }
  }
})
