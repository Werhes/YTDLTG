# downloader.py
import yt_dlp
import os
import asyncio
from config import DOWNLOAD_DIR

# Создаем папку для загрузок, если её нет
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def sync_download(url: str, format_type: str, user_id: int) -> str:
    """Синхронная функция скачивания через yt-dlp"""
    output_template = f"{DOWNLOAD_DIR}/{user_id}_%(id)s.%(ext)s"
    
    ydl_opts = {
        'outtmpl': output_template,
        'quiet': True,
        # Маскировка под мобильный клиент (помогает от базовых блокировок YouTube)
        'extractor_args': {'youtube': ['client=android,ios']},
        
        # ЕСЛИ ЮТУБ СНОВА НАЧНЕТ БЛОКИРОВАТЬ - раскомментируй строку ниже 
        # и положи cookies.txt в папку с ботом
        # 'cookiefile': 'cookies.txt', 
    }

    if format_type == "mp3":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        # Настройка разрешений для видео
        res_map = {"1080p": 1080, "720p": 720, "480p": 480}
        height = res_map.get(format_type, 720)
        
        # Жестко требуем MP4
        ydl_opts['format'] = f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best'
        ydl_opts['merge_output_format'] = 'mp4'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
        # Корректируем расширение файла после обработки FFmpeg
        if format_type == "mp3":
            filename = os.path.splitext(filename)[0] + '.mp3'
        else:
            filename = os.path.splitext(filename)[0] + '.mp4'
            
        return filename

async def download_media(url: str, format_type: str, user_id: int) -> str:
    """Асинхронная обертка: запускает скачивание в отдельном потоке, чтобы бот не вис"""
    return await asyncio.to_thread(sync_download, url, format_type, user_id)