import Coralogix from 'coralogix-logger'

let loggerConfig = null
let logger = null

if (process.env.VUE_APP_FRONTEND_APP_NAME &&
    process.env.VUE_APP_FRONTEND_LOGGER_KEY) {
  // Initialize with Coralogix
  loggerConfig = new Coralogix.LoggerConfig({
    applicationName: process.env.VUE_APP_FRONTEND_APP_NAME,
    privateKey: process.env.VUE_APP_FRONTEND_LOGGER_KEY,
    subsystemName: 'frontend'
  })
  Coralogix.CoralogixLogger.configure(loggerConfig)
  logger = new Coralogix.CoralogixLogger('FrontEnd')
}

function logError (fileName = '', funcName = '', errorMessage = '') {
  if (logger !== null) {
    const error = new Coralogix.Log({
      severity: Coralogix.Severity.error,
      className: fileName,
      methodName: funcName,
      text: errorMessage
    })

    logger.addLog(error)
  } else {
    // Just use a standard console error
    console.warn(errorMessage)
  }
}

export default logError
