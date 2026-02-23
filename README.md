# 🎮 YouTube Shorts Avtomatik Generator — O'rnatish Qo'llanmasi

## Kerakli dasturlar

```bash
pip install openai edge-tts moviepy requests \
            google-auth google-auth-oauthlib google-api-python-client
```

---

## 1-qadam: OpenAI API kaliti

1. https://platform.openai.com/api-keys ga kiring
2. "Create new secret key" bosing
3. Kalitni nusxalab `youtube_shorts_bot.py` ichidagi `OPENAI_API_KEY` ga joylashtiring

---

## 2-qadam: Google / YouTube API

1. https://console.cloud.google.com ga kiring
2. Yangi loyiha oching (yoki mavjudini tanlang)
3. **APIs & Services → Enable APIs** → "YouTube Data API v3" ni yoqing
4. **APIs & Services → Credentials** → "OAuth 2.0 Client ID" yarating
   - Application type: **Desktop app**
5. `client_secrets.json` faylini yuklab oling
6. Bu faylni `youtube_shorts_bot.py` bilan bir papkaga qo'ying

---

## 3-qadam: Ishga tushirish

```bash
python youtube_shorts_bot.py
```

Birinchi ishga tushirganda brauzer ochiladi — YouTube akkauntingizga kiring va ruxsat bering.
Keyingi safar `token.json` fayli orqali avtomatik kiradi.

---

## Sozlamalar (youtube_shorts_bot.py tepasida)

| O'zgaruvchi     | Tavsif                         | Misol                      |
|-----------------|-------------------------------|----------------------------|
| `OPENAI_API_KEY`| OpenAI sir kaliti              | `"sk-..."`                 |
| `TOPIC`         | Video mavzusi                  | `"PUBG sirlari"`           |
| `TTS_VOICE`     | O'zbek ovozi (Edge-TTS)        | `"uz-UZ-MadinaNeural"`     |
| `OUTPUT_DIR`    | Fayllar saqlanadigan papka     | `Path("output")`           |
| `CLIENT_SECRETS`| Google OAuth fayli             | `"client_secrets.json"`    |

---

## Mavjud O'zbekcha ovozlar (Edge-TTS)

```
uz-UZ-MadinaNeural   — Ayol ovozi (tavsiya etiladi)
uz-UZ-SardorNeural   — Erkak ovozi
```

Boshqa ovozlarni ko'rish uchun:
```bash
edge-tts --list-voices | grep uz
```

---

## Chiqish fayllari (`output/` papkasi)

```
output/
├── narration.mp3      ← O'zbekcha ovoz
├── image_1.jpg        ← AI rasm 1
├── image_2.jpg        ← AI rasm 2
├── image_3.jpg        ← AI rasm 3
└── shorts_video.mp4   ← Tayyor video (YouTube ga yuklangan)
```

---

## Tez-tez so'raladigan savollar

**❓ "quota exceeded" xatosi chiqsa?**
OpenAI hisobingizda kredit yo'q. https://platform.openai.com/usage ga kiring.

**❓ Rasm yuklanmasa?**
Pollinations.ai vaqti-vaqti bilan sekin ishlaydi. Biroz kutib qaytadan urining.

**❓ Video sifatini oshirish?**
`step4_create_video()` ichida `preset="slow"` va `fps=60` ga o'zgartiring.

**❓ Har kuni avtomatik ishga tushirish?**
Linux/Mac: `crontab -e` ga qo'shing:
```
0 9 * * * cd /dastur/papkasi && python youtube_shorts_bot.py
```
Windows: Task Scheduler ishlatng.
