const { HttpsProxyAgent } = require('https-proxy-agent');
const https = require('https');
const { logError, logInfo } = require('./logger');

async function testProxyConnection(host, port, username, password) {
  let proxyUrl = `http://${host}:${port}`;
  if (username && password) {
    proxyUrl = `http://${username}:${password}@${host}:${port}`;
  }

  logInfo(`🧪 Test edilecek proxy: ${proxyUrl}`);
  const agent = new HttpsProxyAgent(proxyUrl);

  return new Promise((resolve) => {
    https.get("https://api.ipify.org?format=json", { agent, timeout: 5000 }, (res) => {
      let data = "";
      res.on("data", chunk => data += chunk);
      res.on("end", () => {
        if (res.statusCode === 200) {
          logInfo(`✅ Proxy test başarılı: ${data}`);
          resolve(true);
        } else {
          logError(`🛑 Proxy HTTP kodu: ${res.statusCode}`);
          resolve(false);
        }
      });
    }).on("error", (err) => {
      logError(`Proxy bağlantı hatası: ${err.message}`);
      resolve(false);
    });
  });
}

module.exports = { testProxyConnection };