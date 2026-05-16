from keyboards import get_format_kb, get_start_kb, get_cancel_kb
from downloader import download_media, CANCEL_TASKS
import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import get_format_kb, get_start_kb 
from downloader import download_media
from config import MAX_SIZE_MB

router = Router()

class DownloadState(StatesGroup):
    url = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    # ДОБАВЛЕНО: прикрепляем клавиатуру к приветствию
    await message.answer(
        "👋 Привет! Отправь мне ссылку на YouTube видео.\n\n"
        "Если что-то пошло не так, нажми кнопку ниже.",
        reply_markup=get_start_kb()
    )

# ДОБАВЛЕНО: Обработчик для кнопки "Поддержка"
@router.callback_query(F.data == "support")
async def handle_support(callback: CallbackQuery):
    text = (
        "🛠 **Служба поддержки**\n\n"
        "Бот работает нестабильно? Скорее всего, YouTube снова обновил свои алгоритмы защиты.\n\n"
        "Напиши разработчику: `@WerhesDev`\n"
        "Или открой Issue на GitHub: `https://github.com/Werhes/YTDLTG/issues`"
    )
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer() # Обязательно: закрывает "часики" загрузки на самой кнопке

# ... дальше идет твой старый код @router.message(F.text.regexp...
# Ловим ссылки на YouTube
@router.message(F.text.regexp(r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+'))
async def handle_url(message: Message, state: FSMContext):
    # Сохраняем ссылку в память бота для конкретного пользователя
    await state.update_data(url=message.text)
    await message.answer("🔗 Ссылочка принята! Выбери форматоchek и качество:", reply_markup=get_format_kb())

# Обрабатываем нажатия на кнопки (выбор формата)
@router.callback_query(F.data.startswith("dl_"))
async def handle_format_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    
    if not url:
        await callback.message.edit_text("❌ Ссылка устарела. Отправь ее заново.")
        return

    # ВОТ ТА САМАЯ СТРОКА, КОТОРАЯ СЛУЧАЙНО УДАЛИЛАСЬ:
    format_type = callback.data.replace("dl_", "")
    
    # Выводим кнопку отмены во время скачивания
    await callback.message.edit_text("⏳ Начинаю скачивание... Пожалуйста, подожди.", reply_markup=get_cancel_kb())

    try:
        # Запускаем загрузку
        file_path = await download_media(url, format_type, callback.from_user.id)
        
        # Проверяем размер файла
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > MAX_SIZE_MB:
            await callback.message.edit_text(
                f"❌ Файл слишком большой ({file_size_mb:.1f} MB).\n"
                f"Лимит Telegram: 50 MB. Попробуй выбрать качество похуже."
            )
            os.remove(file_path)
            return

        await callback.message.edit_text("📤 Файл готов! Отправляю в чат...")
        
        # Отправляем файл
        media_file = FSInputFile(file_path)
        if format_type == "mp3":
            await callback.message.answer_audio(media_file)
        else:
            await callback.message.answer_video(media_file)
            
        await callback.message.delete()
        
        # Удаляем файл с жесткого диска после отправки
        os.remove(file_path)
        await state.clear()

    except Exception as e:
        if "DOWNLOAD_CANCELLED" in str(e):
            await callback.message.edit_text("🛑 Скачивание отменено пользователем.")
        else:
            await callback.message.edit_text(f"❌ Ошибка скачивания: {str(e)[:150]}")