# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_format_kb() -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с выбором качества"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 1080p (MP4)", callback_data="dl_1080p")],
        [InlineKeyboardButton(text="🎬 720p (MP4)", callback_data="dl_720p")],
        [InlineKeyboardButton(text="🎬 480p (MP4)", callback_data="dl_480p")],
        [InlineKeyboardButton(text="🎵 Только звук (MP3)", callback_data="dl_mp3")]
    ])
    return kb