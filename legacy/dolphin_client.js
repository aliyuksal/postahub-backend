// inbox_bot/dolphin_client.js
// en üste ekle
const axios = require('axios');
require('dotenv').config({ path: '../.env' }); // gerekiyorsa yol düzelt
const { getRandomUserAgent } = require('../inbox_bot/user_agents');


const DOLPHIN_API_URL = 'https://dolphin-anty-api.com/browser_profiles';
const DOLPHIN_API_TOKEN = process.env.DOLPHIN_API_TOKEN;

const HEADERS = {
  Authorization: `Bearer ${DOLPHIN_API_TOKEN}`,
  'Content-Type': 'application/json',
};

// 🔎 Profil var mı?
async function dolphinProfileExists(profileId) {
  try {
    const res = await axios.get('http://localhost:3001/v1.0/browser_profiles');
    const profiles = res.data?.profiles || [];

    return profiles.some(p => p.uuid === profileId);
  } catch (err) {
    console.error("❌ Dolphin profil kontrol hatası:", err.message);
    return false;
  }
}

// 🆕 Yeni profil oluştur
async function createDolphinProfile(email, userAgent, proxyId = null) {
  const profileName = `profile_${email.replace(/[@.]/g, '_')}`;

  // Kullanıcıdan gelmişse onu, yoksa rastgele seç
  const selectedUA = userAgent || getRandomUserAgent();

  const payload = {
    name: profileName,
    platform: 'windows',
    browserType: 'anty',
    mainWebsite: 'google',
    tags: ['warmup', 'auto'],
    tabs: ['https://google.com'],
    useragent: {
      mode: selectedUA ? 'manual' : 'default',
      value: selectedUA || '',
    },
    timezone: {
      mode: 'manual',
      value: 'Europe/Istanbul',
    },
    locale: {
      mode: 'manual',
      value: 'en_US',
    },
    screen: {
      mode: 'manual',
      resolution: '1920x1080',
    },
    webrtc: { mode: 'altered' },
    canvas: { mode: 'noise' },
    webgl: { mode: 'noise' },
    notes: {
      icon: 'info',
      color: 'blue',
      style: 'outline',
      content: 'Auto-created warmup profile',
    },
    doNotTrack: 1,
  };

  // Proxy varsa proxy bilgilerini veritabanından al ve payload'a ekle
  if (proxyId) {
    try {
      const proxy = await getProxyById(proxyId);
      if (proxy?.host && proxy?.port && proxy?.type) {
        payload.proxy = {
          type: proxy.type, // "http" veya "socks5"
          host: proxy.host,
          port: parseInt(proxy.port),
          login: proxy.username,
          password: proxy.password,
          name: `${proxy.host}:${proxy.port}`,
        };
      } else {
        console.warn("⚠️ Proxy bilgisi eksik, payload.proxy eklenmedi.");
      }
    } catch (err) {
      console.warn("⚠️ Proxy DB sorgusunda hata:", err.message);
    }
  }

  try {
    const response = await axios.post(DOLPHIN_API_URL, payload, { headers: HEADERS });
    return response.data;
  } catch (err) {
    console.error("❌ Dolphin profil oluşturulamadı:", err?.response?.data || err.message);
    throw err;
  }
}

// 🔌 proxy tablosundan çek (PostgreSQL)
const { pool } = require('../inbox_bot/modules/db');
async function getProxyById(proxyId) {
  const res = await pool.query(`SELECT * FROM proxies WHERE id = $1`, [proxyId]);
  if (res.rows.length === 0) throw new Error(`Proxy ${proxyId} bulunamadı`);
  return res.rows[0];
}

module.exports = {
  dolphinProfileExists,
  createDolphinProfile,
};