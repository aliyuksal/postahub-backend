// inbox_bot/modules/gmail_session.js
const { query } = require("./db");
const { logInfo, logError } = require("./logger");

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function isLoggedIn(page) {
  try {
    await page.goto("https://mail.google.com/mail/u/0/#inbox", { waitUntil: "domcontentloaded" });
    await delay(3000);

    const signInBtn = await page.$('a.button[href*="signinchooser"]');
    const currentUrl = page.url();
    const pageContent = await page.content();

    const isSignedOut =
      signInButton !== null ||
      currentUrl.includes("accounts.google.com") ||
      pageContent.includes("Sign in") ||
      pageContent.toLowerCase().includes("to continue to gmail");

    if (isSignedOut) {
      logInfo("🔐 Kullanıcı giriş yapmamış (Sign in butonu görünüyor).");
    }

    return !isSignedOut;
  } catch (err) {
    logError(`🔐 Oturum kontrolü sırasında hata: ${err.message}`);
    return false;
  }
}

async function loginToGmail(page, email, password, recovery_email) {
  try {
    logInfo(`🔐 Gmail'e giriş yapılıyor: ${email}`);

    // Gmail ana sayfasına git, eğer 'Sign in' butonu varsa tıkla
    await page.goto("https://mail.google.com/mail/u/0/#inbox", { waitUntil: "networkidle2" });
    await delay(3000);

    const signInBtn = await page.$('a[href*="ServiceLogin"]');
    if (signInBtn) {
      logInfo("🔘 Sağ üstteki 'Sign in' butonuna tıklanıyor...");
      await signInBtn.click();
      await delay(3000);
    }

    // Şimdi login sayfasında devam et
    await page.goto("https://accounts.google.com/", { waitUntil: "networkidle2" });
    await delay(3000);
    console.log("🌐 Sayfa URL (başlangıç):", page.url());

    // Mevcut hesap seçme ekranı varsa tıkla
    const existingAccount = await page.$('div[data-email]');
    if (existingAccount) {
      logInfo("👤 Mevcut hesap seçiliyor...");
      await existingAccount.click();
      await delay(3000);
      console.log("🌐 Sayfa URL (hesap tıklama sonrası):", page.url());
    }

    // Eğer hala email girişi gerekiyorsa
    const emailField = await page.$('input[type="email"]');
    if (emailField) {
      logInfo("📧 Email giriliyor...");
      await emailField.type(email);
      await page.keyboard.press("Enter");
      await delay(3000);
    }

    // Şifre alanı beklenir ve girilir
    const passwordField = await page.waitForSelector('input[type="password"]', { timeout: 10000 });
    if (passwordField) {
      logInfo("🔐 Şifre giriliyor...");
      await passwordField.type(password);
      await page.keyboard.press("Enter");
      await delay(5000);
    }

    // Recovery adımı otomasyonu
    try {
      console.log("🧠 Recovery seçenekleri kontrol ediliyor...");

      const options = await page.$$('li div');
      let clicked = false;

      for (const option of options) {
        const text = await page.evaluate(el => el.innerText?.toLowerCase(), option);
        if (text && text.includes("confirm your recovery email")) {
          await option.click();
          console.log("✅ 'Confirm your recovery email' seçeneğine tıklandı.");
          clicked = true;
          break;
        }
      }

      if (clicked) {
        await delay(3000);
        const recoveryInput = await page.waitForSelector('input[type="email"], input[aria-label]', { timeout: 7000 });
        if (recoveryInput) {
          console.log("✍️ Recovery email giriliyor...");
          await recoveryInput.type(recovery_email);
          await page.keyboard.press("Enter");
          await delay(4000);
        }
      } else {
        console.log("ℹ️ Recovery adımı görünmedi, devam ediliyor.");
      }
    } catch (e) {
      console.warn("⚠️ Recovery email ekranı işlenemedi:", e.message);
    }

    logInfo("✅ Giriş tamamlandı.");
  } catch (err) {
    logError(`❌ Giriş işlemi başarısız: ${err.message}`);
    throw err;
  }
}

async function saveCookiesToDb(page, email) {
  const cookies = await page.cookies();
  const jsonCookies = JSON.stringify(cookies);

  await query("UPDATE gmail_profiles SET cookies = $1 WHERE email = $2", [jsonCookies, email]);
  logInfo(`💾 Cookie veritabanına kaydedildi: ${email}`);
}

module.exports = {
  isLoggedIn,
  loginToGmail,
  saveCookiesToDb
};