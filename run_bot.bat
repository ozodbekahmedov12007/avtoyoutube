@echo off
cd /d "C:\Users\user\Desktop\files (7)"
call venv\Scripts\activate
python youtube_shorts_bot.py >> logs\bot_log.txt 2>&1
