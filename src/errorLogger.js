import Coralogix from 'coralogix-logger'

const loggerConfig = process.env.VUE_APP_FRONTEND_LOGGER_KEY
  ? new Coralogix.LoggerConfig({
    applicationName: 'streetwise-stage',
    privateKey: process.env.VUE_APP_FRONTEND_LOGGER_KEY,
    subsystemName: 'frontend'
  }) : null

if (loggerConfig !== null) {
  Coralogix.CoralogixLogger.configure(loggerConfig)
}

const logger = (loggerConfig !== null)
  ? new Coralogix.CoralogixLogger('FrontEnd') : null

function logError (fileName = '', funcName = '', errorMessage = '') {
  if (loggerConfig === null) return

  const error = new Coralogix.Log({
    severity: Coralogix.Severity.error,
    className: fileName,
    methodName: funcName,
    text: errorMessage
  })

  logger.addLog(error)
}

export default logError
