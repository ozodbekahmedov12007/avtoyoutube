import os, time, asyncio, random
from pathlib import Path
import schedule
from dotenv import load_dotenv

from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, vfx
from moviepy.config import change_settings

# .env fayldan parollarni o'qish
load_dotenv()



import platform
from moviepy.config import change_settings
import platform
from moviepy.config import change_settings

if platform.system() == "Windows":
    # O'z kompyuteringiz uchun yo'l
    IMAGEMAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
else:
    # Linux Server (Render/Kamatera) uchun
    IMAGEMAGICK_PATH = "/usr/bin/convert"

change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})

# Tizimni tekshirish
if platform.system() == "Windows":
    # O'z kompyuteringiz uchun (Papka nomini tekshiring!)
    IMAGEMAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe" 
else:
    # Linux Server (Oracle/Kamatera) uchun
    IMAGEMAGICK_PATH = "/usr/bin/convert"


change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})
import yt_dlp
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

TTS_VOICE = "en-US-AndrewNeural"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
TEST_MODE = False

# SHU YERDA PUBG_TOPICS BOR
PUBG_TOPICS = [
    "Top 3 hidden sniper spots in Erangel map",
    "How to win every close range combat in PUBG Mobile",
    "Secret aggressive gameplay tactics",
    "Best weapon combinations for Miramar desert",
    "How to survive the final blue zone circle",
    "Pro tips for using grenades in PUBG"
]


def generate_ai_content(topic):
    from groq import Groq
    print(f"\n🧠 [1/5] Groq AI ishga tushdi. Mavzu: {topic}")
    try:
        client = Groq(api_key=GROQ_API_KEY)
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system",
                       "content": "You are a professional PUBG YouTuber. Write a 15-second high-energy script in English. No emojis, no hashtags. Maximum 30 words."},
                      {"role": "user", "content": f"Write a short script about {topic}"}],
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

import os

# Faylning server ichidagi aniq manzilini topamiz
base_dir = os.path.dirname(os.path.abspath(__file__))
cookie_file = os.path.join(base_dir, 'youtube_cookies.txt')

def download_gameplay():
    print("📥 [3/5] Gameplay yuklanmoqda...")

    queries = [
        "PUBG Mobile full gameplay no commentary 1080p",
        "PUBG Mobile high kill gameplay no commentary 4k",
        "PUBG Mobile long gameplay no facecam"
    ]

    query = random.choice(queries)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_file = os.path.join(base_dir, 'youtube_cookies.txt')

    ydl_opts = {
        'cookiefile': cookie_file,
        'format': 'bestvideo[height<=720]+bestaudio/best',
        'noplaylist': True,
        'quiet': False,
        'outtmpl': str(OUTPUT_DIR / 'bg_video.%(ext)s')
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            video_path = ydl.prepare_filename(info['entries'][0])
            return video_path
    except Exception as e:
        print(f"❌ Yuklashda xato: {e}")
        return None try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch40:{query}", download=False)
            valid_videos = [e for e in info['entries'] if e and 60 <= e.get('duration', 0) <= 1200]

            if not valid_videos:
                info = ydl.extract_info("ytsearch10:PUBG Mobile gameplay", download=False)
                valid_videos = [e for e in info['entries'] if e]

            video = random.choice(valid_videos)
            print(f"✅ Tanlandi: {video['title']}")
            ydl.download([video['webpage_url']])
            return str(OUTPUT_DIR / 'background.mp4')
    except Exception as e:
        print(f"❌ Yuklashda xato: {e}")
        return None


def create_shorts_video(bg_path, audio_path, script_text):
    print("🎞️ [4/5] 720p (RAM tejamkor) render boshlandi...")
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
    # 1. Oldindan tayyorgarlik (08:30 yoki 18:30 da boshlanadi)
    print(f"\n⏳ [{time.strftime('%H:%M:%S')}] Ish boshlandi. Tayyorgarlik ko'rilmoqda...")

    # Mavzuni funksiyaning eng boshida tanlab olamiz
    topic = random.choice(PUBG_TOPICS)

    # AI ssenariy va ovoz
    script = generate_ai_content(topic)
    audio_file = asyncio.run(text_to_speech(script))

    # Gameplay yuklash
    bg_video = download_gameplay()

    if bg_video and os.path.exists(bg_video):
        # Video render (bu vaqt oladi)
        final_video_path = create_shorts_video(bg_video, audio_file, script)

        # 2. ANIQ VAQTNI KUTISH REJIMI
        current_hour = time.localtime().tm_hour
        # Agar hozir soat 8:30-9:00 bo'lsa target 9, agar 18:30-19:00 bo'lsa target 19
        target_hour = 9 if current_hour < 12 else 19

        print(f"✅ Video tayyor! Soat roppa-rosa {target_hour}:00:00 bo'lishi kutilmoqda...")

        while True:
            now = time.localtime()
            # Soat millari aynan target_hour:00 bo'lganda sikldan chiqadi
            if now.tm_hour == target_hour and now.tm_min == 0:
                break
            time.sleep(1)  # Har soniyada vaqtni tekshiradi

        # 3. YUKLASH (Endi 'topic' bu yerda ishlaydi)
        youtube_url = upload_to_youtube(final_video_path, topic)
        print(f"\n🚀 SOAT {target_hour}:00! Video muvaffaqiyatli yuklandi: {youtube_url}")

        # 4. TOZALASH (Cleanup)
        print("🧹 Xotira tozalanmoqda...")
        for f in [audio_file, bg_video, final_video_path]:
            if f and os.path.exists(f):
                os.remove(f)
    else:
        # Agar video topilmasa, kutib turgan audio faylni o'chirib tashlaymiz
        if os.path.exists(audio_file):
            os.remove(audio_file)
        print("❌ Sifatli manba topilmadi. Keyingi taymerni kuting.")

def main():
    print("=" * 60)
    print("🤖 PUBG AI BOT (QAROQCHI VERSIYA) ISHGA TUSHDI")
    print("=" * 60)

    # 1. Hozir bitta video yasab ko'rish
    job_create_and_upload_video()

    # 2. Taymerlar
    schedule.every().day.at("09:00").do(job_create_and_upload_video)
    schedule.every().day.at("19:00").do(job_create_and_upload_video)

    while True:
        schedule.run_pending()
        time.sleep(60)

import http.server
import socketserver
import threading

def run_dummy_server():
    # Render beradigan PORT-ni band qilamiz
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Render uchun soxta port {port} ochildi.")
        httpd.serve_forever()

# Serverni orqa fonda (background) ishga tushirish
threading.Thread(target=run_dummy_server, daemon=True).start()

if __name__ == "__main__":
    main()
