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
    let sessionHash = localStorage.getItem('streetwiseSession') || null
    return $axios.post(`vote/`, {
      session_hash: sessionHash,
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
        return response.data
      }
      alert(response.statusText)
      console.log(response.data)
      return null
    })
  },

  saveSurvey (surveyData) {
    let sessionHash = localStorage.getItem('streetwiseSession') || null
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
      console.log(response.data)
      return null
    })
  },

  getRandomImages () {
    return $axios.get(`image/random`)
      .then(response => response.data)
  }
}
