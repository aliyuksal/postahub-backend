// inbox_bot/puppeteer_controller.js
const puppeteer = require("puppeteer");
const { initializeProfile } = require("./modules/profile_initializer");
const { isLoggedIn, loginToGmail, saveCookiesToDb } = require("./modules/gmail_session");
const { query } = require("./modules/db");
const { logInfo, logError } = require("./modules/logger");
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
const { handleInboxReply } = require("./modules/inbox_handler");
require('dotenv').config();
const { sendEngagementLog } = require('./modules/engagement_logger');

const email = process.argv[2];

(async () => {
  if (!email) {
    console.log("❗ Kullanım: node puppeteer_controller.js example@gmail.com");
    return;
  }

  try {
    logInfo(`Başlatılıyor: ${email}`);

    // 1. Profil oluşturulup başlatılıyor
    const { dolphinProfileId, wsUrl, proxyIp, dolphinUserAgent } = await initializeProfile(email);

    // 2. Giriş bilgilerini veritabanından al
    const res = await query("SELECT * FROM gmail_profiles WHERE email = $1", [email]);
    if (res.rowCount === 0) throw new Error("Gmail profili bulunamadı.");

    const profile = res.rows[0];
    const password = profile.password;
    const recovery_email = profile.recovery_email;

    // 3. Puppeteer bağlantısı
    const browser = await puppeteer.connect({ browserWSEndpoint: wsUrl });
    const page = await browser.newPage();

    // 4. Choose an account sayfası kontrolü (profil yüklüyse ama oturum açık değilse)
    await page.goto("https://accounts.google.com/", { waitUntil: "domcontentloaded" });
    await delay(3000);

    const accountButton = await page.$('div[data-email]');
    if (accountButton) {
      logInfo("👤 'Choose an account' ekranı algılandı, hesaba tıklanıyor...");
      await accountButton.click();
      await delay(4000);
    }

    // 5. Gmail oturum kontrol
    const loggedIn = await isLoggedIn(page);
    if (loggedIn) {
      logInfo(`✅ Oturum açık: ${email}`);
    } else {
      // 6. Oturum kapalıysa giriş yap
      await loginToGmail(page, email, password, recovery_email);

      // 7. Giriş sonrası cookie'leri kaydet
      await saveCookiesToDb(page, email);
    }

    // ✅ 8. Mail kontrol ve yanıt
      await handleInboxReply(page, email);

    await browser.disconnect();
    logInfo(`✅ Puppeteer işlemi tamamlandı: ${email}`);
  } catch (err) {
    logError(`❌ Genel hata: ${err.message}`);
  }
})();