// inbox_bot/modules/dolphin_creator.js
const axios = require("axios");
require("dotenv").config();
const { logInfo, logError } = require("./logger");

async function createDolphinProfile(email, proxy, userAgent) {
  const payload = {
    name: email,
    platform: "windows",
    platformVersion: "10.0.0",
    browserType: "anty",
    tags: ["warmup", "auto"],
    tabs: ["https://google.com"],
    mainWebsite: "google",
    useragent: {
      mode: "manual",
      value: userAgent
    },
    webrtc: { mode: "altered" },
    canvas: { mode: "noise" },
    webgl: { mode: "noise" },
    webglInfo: {
      mode: "manual",
      vendor: "Intel Inc.",
      renderer: "Intel Iris OpenGL Engine",
      webgl2Maximum: {
        MAX_SAMPLES: 8,
        MAX_DRAW_BUFFERS: 8,
        MAX_TEXTURE_SIZE: 16384,
        MAX_ELEMENT_INDEX: 4294967294,
        MAX_VIEWPORT_DIMS: [16384, 16384]
      }
    },
    notes: {
      icon: "info",
      color: "blue",
      style: "outline",
      content: "Auto-created warmup profile"
    },
    timezone: { mode: "manual", value: "Europe/Istanbul" },
    locale: { mode: "manual", value: "en_US" },
    geolocation: { mode: "manual", latitude: 41.0082, longitude: 28.9784 },
    cpu: { mode: "manual", value: 4 },
    memory: { mode: "manual", value: 8 },
    doNotTrack: 1,
    proxy: {
      type: proxy.type || "http",
      host: proxy.host,
      port: proxy.port,
      login: proxy.username,
      password: proxy.password,
      name: "My Custom Proxy"
    },
    macAddress: { mode: "random" },
    screen: { mode: "manual", resolution: "1920x1080" },
    newHomepages: [{
      name: "Facebook",
      url: "https://facebook.com",
      mainWebsite: "facebook",
      order: 1
    }]
  };

  const response = await axios.post(
    "https://dolphin-anty-api.com/browser_profiles",
    payload,
    {
      headers: {
        Authorization: `Bearer ${process.env.DOLPHIN_API_TOKEN}`,
        "Content-Type": "application/json"
      }
    }
  );

  const profileId = response.data.browserProfileId;
  logInfo(`📦 Cloud profili oluşturuldu: ID ${profileId}`);

  // Local senkronizasyon için bekleme
  await new Promise(resolve => setTimeout(resolve, 5000));

  return profileId.toString(); // Local API bu ID'yi kullanıyorsa bu dönecek
}

module.exports = { createDolphinProfile };