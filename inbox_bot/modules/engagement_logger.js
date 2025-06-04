const fetch = require("node-fetch");
require("dotenv").config();

const API_URL = process.env.API_BASE_URL || "http://localhost:8000";

async function sendEngagementLog(payload) {
  try {
    const res = await fetch(`${API_URL}/log-engagement`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const json = await res.json();
    console.log("✅ Engagement log gönderildi:", json);
    return json;
  } catch (err) {
    console.error("❌ Engagement log gönderilemedi:", err.message);
    return null;
  }
}

module.exports = { sendEngagementLog };