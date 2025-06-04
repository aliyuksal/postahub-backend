// inbox_bot/handle_gmail.js

const { generateAIReply } = require('./ai_reply');
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function handleGmailLoginAndReply(browser, email, password, recoveryEmail, profileId) {
  const page = await browser.newPage();

  try {
    console.log(`📧 [${email}] Gmail giriş işlemi başlıyor...`);

    await page.goto('https://accounts.google.com/signin/v2/identifier', { waitUntil: 'networkidle2' });

    // Email gir
    await page.waitForSelector('input[type="email"]');
    await page.type('input[type="email"]', email);
    await page.keyboard.press('Enter');
    await delay(3000);

    // Şifre gir
    await page.waitForSelector('input[type="password"]', { visible: true });
    await page.type('input[type="password"]', password);
    await page.keyboard.press('Enter');
    await delay(5000);

    // Recovery ekranını geç
    console.log("🔎 Recovery kontrolü...");
    await page.evaluate(() => {
      const keywords = ["confirm your recovery email", "kurtarma e-posta"];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
      let node;
      while (node = walker.nextNode()) {
        if (keywords.some(k => node.innerText?.toLowerCase().includes(k))) {
          node.click();
          return;
        }
      }
    });
    await delay(3000);

    // Recovery mail gir
    try {
      const input = await page.$('input[type="email"], input[aria-label]');
      if (input) {
        await input.type(recoveryEmail);
        await page.keyboard.press('Enter');
        await delay(4000);
      }
    } catch {}

    // Gelen kutusuna git
    await page.goto('https://mail.google.com/mail/u/0/#inbox', { waitUntil: 'networkidle2' });
    await delay(5000);

    // Okunmamış mail var mı?
    const unread = await page.$('tr.zE');
    if (!unread) {
      console.log("📭 Okunmamış mail yok.");
      return;
    }

    await unread.click();
    await delay(3000);

    // Mail içeriğini al
    const content = await page.$eval('div.a3s', el => el.innerText);
    console.log("📨 Mail içeriği alındı:", content.slice(0, 100));

    // AI yanıt al
    const reply = await generateAIReply(content);
    console.log("✍️ AI yanıt:", reply.slice(0, 100));

    // Yanıtla butonuna tıkla
    const replyBtn = await page.$('div[aria-label="Reply"], div[data-tooltip="Yanıtla"]');
    if (replyBtn) {
      await replyBtn.click();
      await delay(3000);
    }

    // Yanıt kutusuna yapıştır
    const inputBox = await page.$('div[aria-label="Mesaj gövdesi"], div[contenteditable="true"]');
    if (inputBox) {
      await page.evaluate((el, text) => { el.innerText = text }, inputBox, reply);
    }

    // Gönder
    await page.keyboard.down('Control');
    await page.keyboard.press('Enter');
    await page.keyboard.up('Control');
    console.log("📤 Yanıt gönderildi.");

  } catch (err) {
    console.error("❌ handleGmailLoginAndReply hatası:", err.message);
  } finally {
    await page.close();
  }
}

module.exports = { handleGmailLoginAndReply };