# handlers.py
import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards import get_format_kb
from downloader import download_media
from config import MAX_SIZE_MB

router = Router()

# Машина состояний для сохранения ссылки пользователя
class DownloadState(StatesGroup):
    url = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("👋 Привет! Отправь мне ссылку на YouTube видео. Создатель - @WerhesDev")

# Ловим ссылки на YouTube
@router.message(F.text.regexp(r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+'))
async def handle_url(message: Message, state: FSMContext):
    # Сохраняем ссылку в память бота для конкретного пользователя
    await state.update_data(url=message.text)
    await message.answer("🔗 Ссылочка принята! Выбери форматоchek и качество:", reply_markup=get_format_kb())

# Обрабатываем нажатия на кнопки форматов
@router.callback_query(F.data.startswith("dl_"))
async def handle_format_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    
    if not url:
        await callback.message.edit_text("❌ Ссылка потеряна из памяти чел. Отправь её заново.")
        return

    format_type = callback.data.replace("dl_", "")
    await callback.message.edit_text("⏳ Начинаю скачивание...\n*Пожалуйста, подожди, это может занять время.*", parse_mode="Markdown")

    try:
        # Скачиваем файл
        file_path = await download_media(url, format_type, callback.from_user.id)
        
        # Проверяем размер (Телеграм пропускает только до 50 МБ через обычный API)
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > MAX_SIZE_MB:
            await callback.message.edit_text(
                f"❌ Файл слишком большой ({file_size_mb:.1f} МБ).\n"
                f"Лимит Telegram: 50 МБ. Попробуй выбрать качество похуже."
            )
            os.remove(file_path)
            return

        await callback.message.edit_text("📤 Файл скачан на компик @WerhesDev! Отправляю тебе...")
        
        # Отправляем файл пользователю
        media_file = FSInputFile(file_path)
        if format_type == "mp3":
            await callback.message.answer_audio(media_file)
        else:
            await callback.message.answer_video(media_file)
            
        await callback.message.delete() # Удаляем техническое сообщение
        
        # Подчищаем за собой
        os.remove(file_path)
        await state.clear()

    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка скачивания (возможно видео удалено или защищено):\n`{str(e)[:150]}`", parse_mode="Markdown")