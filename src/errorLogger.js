import Coralogix from 'coralogix-logger'

const loggerConfig = new Coralogix.LoggerConfig({
  applicationName: process.env.VUE_APP_FRONTEND_APP_NAME,
  privateKey: process.env.VUE_APP_FRONTEND_LOGGER_KEY,
  subsystemName: 'frontend'
})

Coralogix.CoralogixLogger.configure(loggerConfig)
const logger = new Coralogix.CoralogixLogger('FrontEnd')

function logError (fileName = '', funcName = '', errorMessage = '') {
  try {
    const error = new Coralogix.Log({
      severity: Coralogix.Severity.error,
      className: fileName,
      methodName: funcName,
      text: errorMessage
    })

    logger.addLog(error)
  } catch (_exception) {
    console.error('Failed to log error on the server. Logging on the console instead', errorMessage)
  }
}

export default logError
