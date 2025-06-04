// inbox_bot/modules/dolphin_starter.js
const axios = require("axios");
const { logInfo, logError } = require("./logger");

const DOLPHIN_API = "http://localhost:3001/v1.0";

async function startProfile(profileId) {
  try {
    await new Promise(resolve => setTimeout(resolve, 5000)); // Senkron bekleme

    const res = await axios.get(`${DOLPHIN_API}/browser_profiles/${profileId}/start?automation=1`);
    console.log("📡 Dolphin yanıtı:", res.data);

    if (
      res.data?.automation?.port &&
      res.data?.automation?.wsEndpoint
    ) {
      const wsUrl = `ws://localhost:${res.data.automation.port}${res.data.automation.wsEndpoint}`;
      logInfo(`🟢 WebSocket oluşturuldu: ${wsUrl}`);
      return wsUrl;
    }

    throw new Error("WebSocket bilgisi eksik: 'port' veya 'wsEndpoint' yok.");
  } catch (err) {
    logError(`❌ Dolphin profil başlatılamadı: ${err.message}`);
    if (err.response?.data) {
      console.error("💥 Dolphin API Hatası:", err.response.data);
    }
    throw err;
  }
}

module.exports = { startProfile };