@echo off
echo ================================================
echo  PUBG YouTube Shorts — Avtomatik Rejalashtirish
echo ================================================
echo.

:: Logs papkasini yaratish
if not exist "C:\Users\user\Desktop\files (7)\logs" (
    mkdir "C:\Users\user\Desktop\files (7)\logs"
    echo [OK] Logs papkasi yaratildi
)

:: run_bot.bat ni to'g'ri joyga ko'chirish
copy /Y "%~dp0run_bot.bat" "C:\Users\user\Desktop\files (7)\run_bot.bat" >nul
echo [OK] run_bot.bat ko'chirildi

echo.
echo [1/2] Soat 09:00 vazifasi qo'shilmoqda...
schtasks /create /tn "PUBG_Shorts_Morning" /tr "\"C:\Users\user\Desktop\files (7)\run_bot.bat\"" /sc daily /st 09:00 /f /rl HIGHEST
if %errorlevel%==0 (echo     [OK] 09:00 vazifasi qo'shildi!) else (echo     [XATO] 09:00 vazifasi qo'shilmadi)

echo.
echo [2/2] Soat 19:00 vazifasi qo'shilmoqda...
schtasks /create /tn "PUBG_Shorts_Evening" /tr "\"C:\Users\user\Desktop\files (7)\run_bot.bat\"" /sc daily /st 19:00 /f /rl HIGHEST
if %errorlevel%==0 (echo     [OK] 19:00 vazifasi qo'shildi!) else (echo     [XATO] 19:00 vazifasi qo'shilmadi)

echo.
echo ================================================
echo  TAYYOR! Endi har kuni 2 ta video yuklanadi:
echo    - Ertalab soat 09:00
echo    - Kechqurun soat 19:00
echo.
echo  Vazifalarni ko'rish: Task Scheduler oching
echo  yoki quyidagi buyruqni kiriting:
echo    schtasks /query /tn "PUBG_Shorts_Morning"
echo    schtasks /query /tn "PUBG_Shorts_Evening"
echo ================================================
echo.
pause
