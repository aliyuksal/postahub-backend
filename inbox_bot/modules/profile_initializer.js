const axios = require("axios");
const { query } = require("./db");
const { testProxyConnection } = require("./proxy_tester");
const { createDolphinProfile } = require("./dolphin_creator");
const { startProfile } = require("./dolphin_starter");
const { logInfo, logError } = require("./logger");
require("dotenv").config();

const DOLPHIN_API = "http://localhost:3001/v1.0";

async function initializeProfile(email) {
  logInfo(`📥 Profil başlatılıyor: ${email}`);

  // 1. Gmail profili çek
  const res = await query("SELECT * FROM gmail_profiles WHERE email = $1", [email]);
  if (res.rowCount === 0) throw new Error("❌ Gmail profili bulunamadı.");
  const profile = res.rows[0];

  // 2. User-Agent kontrolü
  const defaultUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";
  const userAgent = profile.user_agent && profile.user_agent.trim() !== ""
    ? profile.user_agent
    : defaultUserAgent;

  // 3. Proxy seç
  const proxyRes = await query("SELECT * FROM proxies WHERE used = false LIMIT 1");
  if (proxyRes.rowCount === 0) throw new Error("❌ Uygun proxy bulunamadı.");
  const proxy = proxyRes.rows[0];

  // 4. Proxy test et
  const isProxyValid = await testProxyConnection(proxy.host, proxy.port, proxy.username, proxy.password);
  if (!isProxyValid) {
    await query("UPDATE proxies SET used = true WHERE id = $1", [proxy.id]);
    throw new Error("❌ Proxy bağlantısı başarısız, başka proxy denenmeli.");
  }

  // 5. Dolphin profili oluştur (Cloud API)
  const dolphinProfileId = await createDolphinProfile(profile.email, proxy, userAgent);

  if (!dolphinProfileId || typeof dolphinProfileId !== "string") {
    throw new Error("❌ Dolphin profil ID geçersiz (undefined veya NaN).");
  }

  logInfo(`🐬 Dolphin profil ID: ${dolphinProfileId}`);

  // 6. Cookie varsa Local API üzerinden import et
  if (
  profile.cookies &&
  (
    (typeof profile.cookies === "string" && profile.cookies.trim() !== "") ||
    (typeof profile.cookies === "object" && Array.isArray(profile.cookies))
  )
) {
  try {
    const parsedCookies = typeof profile.cookies === "string"
      ? JSON.parse(profile.cookies)
      : profile.cookies;

    await axios.post("http://localhost:3001/v1.0/cookies/import", {
      cookies: parsedCookies,
      profileId: parseInt(dolphinProfileId),
      transfer: 0,
      cloudSyncDisabled: false
    });

    logInfo(`🍪 Cookie başarıyla import edildi.`);
  } catch (err) {
    logError(`⚠️ Cookie import hatası: ${err.message}`);
  }
} else {
  logInfo(`ℹ️  Cookie yok, giriş yapılması gerekecek.`);
}

  // 7. Senkronizasyon için bekle
  await new Promise(resolve => setTimeout(resolve, 5000));

  // 8. Dolphin profilini Local API ile başlat
  const wsUrl = await startProfile(dolphinProfileId);
  logInfo(`🚀 Profil başlatıldı. WebSocket URL alındı.`);

  // 9. Proxy'yi used = true yap
  await query("UPDATE proxies SET used = true WHERE id = $1", [proxy.id]);

  // 10. Başarılı dönüş
  return {
  dolphinProfileId,
  wsUrl,
  proxyIp: proxy.host,
  dolphinUserAgent: userAgent,  // ✨ eksik olan bu
  proxyGeo: proxy.geo_location || null  // ✨ varsa
};
}

module.exports = { initializeProfile };