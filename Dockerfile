FROM python:3.11-slim

# FFmpeg, ImageMagick va Node.js (yt-dlp JavaScript kodlarini o'qishi uchun) o'rnatish
RUN apt-get update && apt-get install -y ffmpeg imagemagick nodejs

WORKDIR /app
COPY . .

# Cookies faylini ko'chirish
COPY youtube_cookies.txt /app/youtube_cookies.txt

# yt-dlp ni eng oxirgi versiyaga majburan yangilash va boshqa kutubxonalarni o'rnatish
RUN pip install --no-cache-dir --upgrade yt-dlp
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "youtube_shorts_bot.py"]