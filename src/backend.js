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

  voteCast (isRight, imageLeft, imageRight, timeTaken) {
    return $axios.post(`vote/`, {
      choice_id: isRight ? imageRight : imageLeft,
      other_id: isRight ? imageLeft : imageRight,
      is_leftimage: (isRight !== null && !isRight),
      is_undecided: (isRight === null),
      time_elapsed: timeTaken
    }).then(function (response) {
      if (response.status === 201) {
        return response
      }
      alert(response.statusText)
      console.log(response.data)
      return null
    }).then(response => response.data)
  },

  getRandomImages () {
    return $axios.get(`image/random`)
      .then(response => response.data)
  }
}
