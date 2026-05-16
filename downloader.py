# downloader.py
import yt_dlp
import os
import asyncio
from config import DOWNLOAD_DIR

# Список пользователей, которые нажали "Отмена"
CANCEL_TASKS = set()

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def sync_download(url: str, format_type: str, user_id: int) -> str:
    output_template = f"{DOWNLOAD_DIR}/{user_id}_%(id)s.%(ext)s"
    
    # Хук, который каждую долю секунды проверяет, не нажал ли юзер отмену
    def check_cancel_hook(d):
        if user_id in CANCEL_TASKS:
            raise Exception("DOWNLOAD_CANCELLED")

    ydl_opts = {
        'outtmpl': output_template,
        'quiet': True,
        'extractor_args': {'youtube': ['client=android,ios']},
        'progress_hooks': [check_cancel_hook], # Подключаем наш хук
    }

    # ... логика форматов остается прежней
    if format_type == "mp3":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
    else:
        res_map = {"1080p": 1080, "720p": 720, "480p": 480}
        height = res_map.get(format_type, 720)
        ydl_opts['format'] = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]/best'
        ydl_opts['merge_output_format'] = 'mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if format_type == "mp3":
                filename = os.path.splitext(filename)[0] + '.mp3'
            else:
                filename = os.path.splitext(filename)[0] + '.mp4'
            return filename
    finally:
        # Убираем юзера из списка отмены после завершения (или обрыва)
        CANCEL_TASKS.discard(user_id)

async def download_media(url: str, format_type: str, user_id: int) -> str:
    return await asyncio.to_thread(sync_download, url, format_type, user_id)