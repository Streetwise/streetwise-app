import axios from 'axios'

let $axios = axios.create({
  baseURL: '/api/',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
})

// Request Interceptor
$axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Fake Token'
  return config
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})

export default {
  voteCast (isRight, imageLeft, imageRight, timeTaken, textComment) {
    const sessionHash = localStorage.getItem('streetwiseSession') || null
    const campaignId = localStorage.getItem('currentCampaignId') || null
    return $axios.post(`vote/`, {

      session_hash: sessionHash,
      campaign_id: campaignId,
      choice_id: isRight ? imageRight : imageLeft,
      other_id: isRight ? imageLeft : imageRight,
      is_leftimage: (isRight !== null && !isRight),
      is_undecided: (isRight === null),
      time_elapsed: timeTaken,
      window_width: window.innerWidth,
      window_height: window.innerHeight,
      comment: textComment

    }).then(function (response) {
      if (response.status === 201) {
        if (typeof response.data.session_hash !== 'undefined' &&
            response.data.session_hash !== sessionHash) {
          localStorage.setItem('streetwiseSession', response.data.session_hash)
        }
        if (typeof response.data.campaign !== 'undefined' &&
            response.data.campaign.id !== campaignId) {
          localStorage.setItem('currentCampaignId', response.data.campaign.id)
        }
        return response.data
      }
      alert(response.statusText)
      console.debug(response.data)
      return null
    })
  },

  saveSurvey (surveyData) {
    const sessionHash = localStorage.getItem('streetwiseSession') || null
    if (!sessionHash) {
      return alert('Session not found, please start again')
    }
    return $axios.post(`vote/survey`, {

      session_hash: sessionHash,
      survey_data: surveyData

    }).then(function (response) {
      if (response.status === 201) {
        return true
      }
      alert(response.statusText)
      console.debug(response.data)
      return null
    })
  },

  getNextCampaign () {
    const campaignId = localStorage.getItem('currentCampaignId') || null
    return $axios.post(`campaign/next`, {

      campaign_id: campaignId

    }).then(function (response) {
      if (response.status === 201) {
        localStorage.setItem('currentCampaignId', response.data.id)
        return response.data
      }
      console.debug('Default campaign selected')
      localStorage.setItem('currentCampaignId', 1)
      return { id: 1 }
    })
  },

  getRandomImages () {
    const campaignId = localStorage.getItem('currentCampaignId') || null
    if (campaignId === null) {
      console.info('Waiting for campaign data ...')
      return null
    }
    return $axios.get(`image/random/` + campaignId)
      .then(response => response.data)
  },

  getVoteCount () {
    return $axios.get(`vote/count`)
      .then(response => response.data)
  }
}
