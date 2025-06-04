import requests
import random
from cleantext import clean
from sqlalchemy.orm import Session
from shared.models.ai_prompt import AIPrompt


def get_random_prompt(db: Session, user_id: int, category: str = None, language: str = None) -> AIPrompt:
    query = db.query(AIPrompt).filter(AIPrompt.user_id == user_id)
    if category:
        query = query.filter(AIPrompt.category == category)
    if language:
        query = query.filter(AIPrompt.language == language)

    prompts = query.all()
    if not prompts:
        return AIPrompt(id=None, user_id=user_id, template="Write a polite, short email to test my inbox deliverability.")

    return random.choice(prompts)


def generate_email_body(prompt: AIPrompt, name: str = "there", surname: str = "") -> str:
    # Alıcı adını oluştur
    recipient_full_name = f"{name} {surname}".strip()

    # AI modeline gönderilecek tam prompt
    full_prompt = f"{prompt.template}\nRecipient: {recipient_full_name}"

    try:
        response = requests.post(
            "http://138.199.198.186:8000/generate",
            json={"prompt": full_prompt},
            timeout=200  # ⏱️  200 saniye
        )

        raw_text = response.json().get("response", "")
        if not raw_text:
            print("⚠️ Empty response from AI.")
            return "Hi, just sending a quick message as part of the warm-up. Talk soon!"

        # 💡 İlk olarak temizleme olmadan test etmek istersen:
        # return raw_text

        # Temizlenmiş içerik döndür
        return clean_email_body(raw_text)

    except Exception as e:
        print(f"❌ Error during AI request: {e}")
        return "Hi, just sending a quick message as part of the warm-up. Talk soon!"


def clean_email_body(text: str) -> str:
    return clean(
        text,
        fix_unicode=True,
        to_ascii=False,
        lower=False,
        normalize_whitespace=True,
        no_line_breaks=True,
        strip_lines=True,
        no_urls=True,
        no_emails=True,
        no_phone_numbers=True,
        no_numbers=False,  # 🔓 sayıları koru (ör: %50)
        no_digits=False,   # 🔓 özellikle indirim kodları için
        no_currency_symbols=False,  # 🔓 $, %, € gibi işaretler kalsın
        no_punct=False,
        no_emoji=True,
        replace_with_url="",
        replace_with_email="",
        replace_with_phone_number="",
        replace_with_number="",
        replace_with_digit="",
        replace_with_currency_symbol="",
        replace_with_punct="",
        lang="en"
    )
