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

  castVote (isRight, imageLeft, imageRight, timeTaken) {
    return $axios.post(`votes/`, {
      choice: isRight ? imageRight : imageLeft,
      other: isRight ? imageLeft : imageRight,
      timetaken: timeTaken,
      is_left: (isRight !== null && !isRight),
      is_undecided: (isRight === null)
    }).then(function (response) {
      if (response.status === 201) {
        return response
      }
      alert(response.statusText)
      console.log(response.data)
      return null
    }).then(response => response.data)
  },

  fetchResource () {
    return $axios.get(`resource/xxx`)
      .then(response => response.data)
  },

  fetchSecureResource () {
    return $axios.get(`secure-resource/zzz`)
      .then(response => response.data)
  }
}
