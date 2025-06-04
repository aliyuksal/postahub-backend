const { query } = require("./db");
const { logInfo, logError } = require("./logger");
const axios = require("axios");
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
require('dotenv').config();
const { sendEngagementLog } = require('./engagement_logger');

async function handleInboxReply(page, senderEmail, meta = {}) {
  const { proxyIp, dolphinUserAgent } = meta;
  try {
    logInfo("\uD83D\uDCE5 Gmail gelen kutusu açılıyor...");

    await page.goto("https://mail.google.com/mail/u/0/#inbox", {
      waitUntil: "domcontentloaded",
      timeout: 0
    });
    await delay(4000);

    const mailRows = await page.$$('tr.zA');
    const unreadMails = [];

    for (const row of mailRows) {
      const className = await row.evaluate(el => el.className);
      if (className.includes('zE')) {
        unreadMails.push(row);
      }
    }

    if (unreadMails.length === 0) {
      logInfo("\uD83D\uDCEC Okunmamış mail bulunamadı.");
      return;
    }

    logInfo(`\uD83D\uDCEC ${unreadMails.length} okunmamış mail bulundu.`);

    for (let i = 0; i < Math.min(unreadMails.length, 5); i++) {
      logInfo(`\uD83D\uDD0D ${i + 1}. mail kontrol ediliyor...`);

      try {
        const freshRows = await page.$$('tr.zA');
        const classFiltered = [];

        for (const row of freshRows) {
          const className = await row.evaluate(el => el.className);
          if (className.includes('zE')) {
            classFiltered.push(row);
          }
        }

        const mail = classFiltered[i];
        if (!mail) {
          logInfo(`⚠️ ${i + 1}. mail bulunamadı.`);
          continue;
        }

        await mail.click();
        await delay(4000);

        await page.evaluate(() => window.scrollBy(0, window.innerHeight));
        await delay(2000);

        const mailContent = await page.$eval("div.a3s", el => el.innerText);
        logInfo("\uD83D\uDCC4 Mail içeriği alındı.");

        const uuidMatch = mailContent.replace(/\s+/g, "").match(/\[uuid:([a-zA-Z0-9-]{36})\]/);
        if (!uuidMatch) {
          logInfo("\uD83D\uDD0D UUID içeren mail değil, atlanıyor.");

          await page.goto("https://mail.google.com/mail/u/0/#inbox", {
            waitUntil: "domcontentloaded",
            timeout: 0
          });
          await delay(4000);
          continue;
        }

        const trackingCode = uuidMatch[1];
        logInfo(`\uD83D\uDD17 Tracking Code bulundu: ${trackingCode}`);

        const res = await query(
          "SELECT * FROM email_logs WHERE tracking_code = $1 AND recipient_email = $2",
          [trackingCode, senderEmail]
        );

        if (res.rowCount === 0) {
          logInfo("⚠️ Eşleşen email_logs kaydı bulunamadı.");

          await page.goto("https://mail.google.com/mail/u/0/#inbox", {
            waitUntil: "domcontentloaded",
            timeout: 0
          });
          await delay(4000);
          continue;
        }

        const originalLog = res.rows[0];

        await sendEngagementLog({
          email_log_id: originalLog.id,
          event_type: "inbox",
          event_time: new Date().toISOString(),
          ai_generated_response: null,
          ip_address: proxyIp || null,
          user_agent: dolphinUserAgent || null,
          geo_location: "TR",
          meta: {
            location: "inbox",
            checked_by: "inbox_bot",
            confidence: 1.0
          }
        });

        const aiApiUrl = process.env.AI_API_URL;

        const aiRes = await axios.post(aiApiUrl, {
          prompt: `Reply this message as friendly email:\n\n${mailContent}`,
        }, { timeout: 200000 });

        const aiReply = aiRes.data.response || "Thanks for your message!";
        logInfo("\uD83E\uDD16 AI yanıtı alındı.");

        let replyBoxExists = await page.$("div[aria-label='Message Body']");

        if (!replyBoxExists) {
          logInfo("✉️ Yanıt kutusu kapalı, açılıyor...");

          const replySelector = 'div[role="button"][data-tooltip="Yanıtla"], div[aria-label="Reply"]';

          try {
            await page.waitForSelector(replySelector, { timeout: 10000 });
            const replyBtn = await page.$(replySelector);

            if (!replyBtn) throw new Error("Reply butonu görünmüyor");

            await replyBtn.evaluate(el => el.scrollIntoView({ behavior: 'smooth', block: 'center' }));
            await delay(1000);
            await replyBtn.click();
            await delay(3000);
            logInfo("✅ Yanıtla butonuna tıklandı.");
          } catch (e) {
            throw new Error("💥 Yanıt kutusu hiçbir yöntemle açılamadı: " + e.message);
          }

          await delay(2000);
        } else {
          logInfo("✅ Yanıt kutusu zaten açık.");
        }

        await page.keyboard.type(aiReply);
        await page.keyboard.down("Control");
        await page.keyboard.press("Enter");
        await page.keyboard.up("Control");

        logInfo("\uD83D\uDCE8 Yanıt gönderildi.");

        await query(`
          INSERT INTO engagement_logs (email_log_id, event_type, event_time, ai_generated_response)
          VALUES ($1, 'reply_sent', NOW(), $2)
        `, [originalLog.id, aiReply]);

        logInfo("\uD83D\uDCDD engagement_logs kaydı tamamlandı.");

        break;
      } catch (innerErr) {
        logError(`⚠️ Mail işlenemedi: ${innerErr.message}`);

        await page.goto("https://mail.google.com/mail/u/0/#inbox", {
          waitUntil: "domcontentloaded",
          timeout: 0
        });
        await delay(4000);
      }
    }
  } catch (err) {
    logError(`❌ Inbox işlem hatası: ${err.message}`);
  }
}

module.exports = { handleInboxReply };
