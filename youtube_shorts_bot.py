import os
import time
import asyncio
import random
import threading
import http.server
import socketserver
from pathlib import Path

import schedule
import yt_dlp
from dotenv import load_dotenv
import platform
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, vfx
from moviepy.config import change_settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ==========================================
# 1. RENDER UCHUN SOXTA SERVER (Eng tepada)
# ==========================================
def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("0.0.0.0", port), Handler) as httpd:
            print(f"🌐 Render uchun {port}-port muvaffaqiyatli ochildi!")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Port ochishda xatolik: {e}")

threading.Thread(target=keep_alive, daemon=True).start()

# ==========================================
# 2. ASOSIY SOZLAMALAR VA PAROLLAR
# ==========================================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

# ImageMagick sozlamalari
if platform.system() == "Windows":
    IMAGEMAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
else:
    IMAGEMAGICK_PATH = "/usr/bin/convert"
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})

TTS_VOICE = "en-US-AndrewNeural"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

PUBG_TOPICS = [
    "Top 3 hidden sniper spots in Erangel map",
    "How to win every close range combat in PUBG Mobile",
    "Secret aggressive gameplay tactics",
    "Best weapon combinations for Miramar desert",
    "How to survive the final blue zone circle",
    "Pro tips for using grenades in PUBG"
]

# ==========================================
# 3. ASOSIY FUNKSIYALAR
# ==========================================
def generate_ai_content(topic):
    from groq import Groq
    print(f"\n🧠 [1/5] Groq AI ishga tushdi. Mavzu: {topic}")
    try:
        client = Groq(api_key=GROQ_API_KEY)
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional PUBG YouTuber. Write a 15-second high-energy script in English. No emojis, no hashtags. Maximum 30 words."},
                {"role": "user", "content": f"Write a short script about {topic}"}
            ],
        )
        script = chat.choices[0].message.content.strip()
        print(f"📝 Ssenariy tayyor: {script[:50]}...")
        return script
    except Exception as e:
        print(f"❌ Groq xatosi: {e}")
        return "Check out these insane PUBG Mobile tactics to dominate the battlefield!"

async def text_to_speech(text):
    import edge_tts
    print("🎙️ [2/5] Ovoz yozilmoqda...")
    audio_path = OUTPUT_DIR / "voice.mp3"
    await edge_tts.Communicate(text, TTS_VOICE).save(str(audio_path))
    return str(audio_path)

def download_gameplay():
    print("📥 [3/5] Tiniq video qidirilmoqda...")
    queries = [
        "PUBG Mobile full gameplay no commentary 1080p",
        "PUBG Mobile high kill gameplay no commentary 4k",
        "PUBG Mobile long gameplay no facecam"
    ]
    query = random.choice(queries)

    # Cookies faylini aniq topish
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_file = os.path.join(base_dir, 'youtube_cookies.txt')
    
    # Saqlanadigan fayl nomi
    out_tmpl = str(OUTPUT_DIR / 'bg_video.%(ext)s')

    ydl_opts = {
        'cookiefile': cookie_file,
        'format': 'bestvideo[ext=mp4]+bestaudio[m4a]/best[ext=mp4]/best',
        'noplaylist': True,
        'quiet': False,
        'outtmpl': out_tmpl,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"🔍 Qidirilmoqda: {query}")
            # ytsearch1 orqali faqat bitta (1-chi) videoni yuklab olamiz
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            
            if 'entries' in info and len(info['entries']) > 0:
                video_info = info['entries'][0]
                downloaded_file = ydl.prepare_filename(video_info)
                print(f"✅ Video yuklandi: {downloaded_file}")
                return downloaded_file
            return None
    except Exception as e:
        print(f"❌ Yuklashda xato: {e}")
        return None

def create_shorts_video(bg_path, audio_path, script_text):
    print("🎞️ [4/5] Render boshlandi (RAM tejamkor rejim)...")
    audio = AudioFileClip(audio_path)
    bg_clip = VideoFileClip(bg_path)

    max_start = max(0, bg_clip.duration - audio.duration - 5)
    start_time = random.uniform(0, max_start)
    bg_clip = bg_clip.subclip(start_time, start_time + audio.duration)

    w, h = bg_clip.size
    target_ratio = 9 / 16
    if w / h > target_ratio:
        new_w = h * target_ratio
        bg_clip = vfx.crop(bg_clip, x_center=w / 2, y_center=h / 2, width=new_w, height=h)

    bg_clip = bg_clip.resize(height=1280)

    words = script_text.split()
    chunks = [' '.join(words[i:i + 3]) for i in range(0, len(words), 3)]
    chunk_dur = audio.duration / len(chunks)

    text_clips = []
    for i, chunk in enumerate(chunks):
        txt = (TextClip(chunk, fontsize=70, color='yellow', font='Arial-Bold',
                        stroke_color='black', stroke_width=2, method='caption',
                        size=(600, None))
               .set_start(i * chunk_dur)
               .set_duration(chunk_dur)
               .set_position(('center', 900)))
        text_clips.append(txt)

    final_video = CompositeVideoClip([bg_clip] + text_clips).set_audio(audio)
    out_path = str(OUTPUT_DIR / "final_pubg_shorts.mp4")

    final_video.write_videofile(
        out_path, fps=30, codec="libx264", bitrate="4000k",
        audio_codec="aac", preset="ultrafast", threads=1, logger=None
    )

    bg_clip.close()
    audio.close()
    return out_path

def upload_to_youtube(video_path, topic):
    print("📤 [5/5] YouTube'ga yuklanmoqda...")
    try:
        creds = Credentials(
            token=None,
            refresh_token=GOOGLE_REFRESH_TOKEN,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET
        )

        yt = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {
                "title": f"{topic} 🎮 #Shorts #PUBG",
                "description": f"Pro tips about {topic} in PUBG Mobile!\n\n#pubgmobile #gaming #shorts",
                "categoryId": "20"
            },
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
        }

        req = yt.videos().insert(
            part="snippet,status", body=body,
            media_body=MediaFileUpload(video_path, chunksize=1024 * 1024, resumable=True)
        )

        response = None
        while response is None:
            status, response = req.next_chunk()
            if status:
                print(f"  📊 Yuklanmoqda: {int(status.progress() * 100)}%", end="\r")

        return f"https://www.youtube.com/shorts/{response['id']}"

    except Exception as e:
        if "uploadLimitExceeded" in str(e):
            print("\n❌ YouTube limiti tugagan! 24 soatdan keyin urinib ko'ring.")
        else:
            print(f"\n❌ Yuklashda xatolik yuz berdi: {e}")
        return "Xatolik tufayli yuklanmadi"


def job_create_and_upload_video():
    print(f"\n⏳ [{time.strftime('%H:%M:%S')}] Ish boshlandi. Tayyorgarlik ko'rilmoqda...")
    topic = random.choice(PUBG_TOPICS)

    script = generate_ai_content(topic)
    audio_file = asyncio.run(text_to_speech(script))
    bg_video = download_gameplay()

    if bg_video and os.path.exists(bg_video):
        final_video_path = create_shorts_video(bg_video, audio_file, script)

        current_hour = time.localtime().tm_hour
        target_hour = 9 if current_hour < 12 else 19

        print(f"✅ Video tayyor! Soat roppa-rosa {target_hour}:00:00 bo'lishi kutilmoqda...")

        while True:
            now = time.localtime()
            if now.tm_hour == target_hour and now.tm_min == 0:
                break
            time.sleep(1)

        youtube_url = upload_to_youtube(final_video_path, topic)
        print(f"\n🚀 SOAT {target_hour}:00! Video muvaffaqiyatli yuklandi: {youtube_url}")

        print("🧹 Xotira tozalanmoqda...")
        for f in [audio_file, bg_video, final_video_path]:
            if f and os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass
    else:
        if os.path.exists(audio_file):
            os.remove(audio_file)
        print("❌ Sifatli manba topilmadi. Keyingi taymerni kuting.")

def main():
    print("=" * 60)
    print("🤖 PUBG AI BOT (QAROQCHI VERSIYA) ISHGA TUSHDI")
    print("=" * 60)

    job_create_and_upload_video()

    schedule.every().day.at("09:00").do(job_create_and_upload_video)
    schedule.every().day.at("19:00").do(job_create_and_upload_video)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()