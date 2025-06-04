// inbox_bot/modules/logger.js
function logInfo(msg) {
  console.log(`ℹ️  ${new Date().toISOString()} - ${msg}`);
}

function logError(msg) {
  console.error(`❌ ${new Date().toISOString()} - ${msg}`);
}

module.exports = { logInfo, logError };