# 1. Asosiy tizim (Python o'rnatilgan tayyor Linux)
FROM python:3.10-slim

# 2. FFmpeg va ImageMagick'ni tekinga, terminalsiz o'rnatish
RUN apt-get update && apt-get install -y ffmpeg imagemagick

# 3. Kodingizni Docker ichiga nusxalash
WORKDIR /app
COPY . .

# 4. Kutubxonalarni o'rnatish (requirements.txt dan)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Botni ishga tushirish komandasi
CMD ["python", "youtube_shorts_bot.py"]