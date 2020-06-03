import Coralogix from 'coralogix-logger'

const loggerConfig = new Coralogix.LoggerConfig({
  applicationName: 'streetwise-stage',
  privateKey: process.env.VUE_APP_FRONTEND_LOGGER_KEY,
  subsystemName: 'frontend'
})

Coralogix.CoralogixLogger.configure(loggerConfig)
const logger = new Coralogix.CoralogixLogger('FrontEnd')

function logError (fileName = '', funcName = '', errorMessage = '') {
  const error = new Coralogix.Log({
    severity: Coralogix.Severity.error,
    className: fileName,
    methodName: funcName,
    text: errorMessage
  })

  logger.addLog(error)
}

export default logError
