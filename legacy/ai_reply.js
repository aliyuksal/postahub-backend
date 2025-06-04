// inbox_bot/ai_reply.js

const axios = require('axios');

// Buraya kendi AI sunucunun endpoint'ini gir
const AI_API_URL = "http://138.199.198.186:8000/generate";

async function generateAIReply(originalText) {
  try {
    const response = await axios.post(AI_API_URL, {
      prompt: `Reply to this email:\n\n${originalText}`
    }, {
      timeout: 200_000
    });

    const reply = response.data?.response?.trim();
    if (!reply) throw new Error("AI response is empty");

    return reply;
  } catch (err) {
    console.error("❌ AI yanıt alınamadı:", err.message);
    return "Thank you for your message. I'll get back to you shortly."; // fallback mesaj
  }
}

module.exports = { generateAIReply };