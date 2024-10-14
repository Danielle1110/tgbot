import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Хранение чисел и счетчик
numbers = []
count = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("/reset")]  # Кнопка для сброса
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Отправь мне число и я напишу тебе среднее значение и порядковый номер. ЕСЛИ ЧТО-ТО РАБОТАЕТ НЕПРАВИЛЬНО НАЖМИ /reset.",
        reply_markup=reply_markup
    )

async def add_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global numbers, count
    try:
        number = int(update.message.text)  # Пробуем преобразовать текст в число
        numbers.append(number)  # Добавляем число в список
        count += 1  # Увеличиваем счетчик
        await update.message.reply_text(f"бой номер: {count}")
        
        # Расчет и отправка среднего значения, округленного до целого
        average = round(sum(numbers) / len(numbers))  # Округляем до целого
        await update.message.reply_text(f"Ты никогда не возьмешь три отметки: {average}")
        
    except ValueError:
        await update.message.reply_text("Пожалуйста, вводите только числа.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global numbers, count
    numbers = []  # Очищаем список чисел
    count = 0  # Сбрасываем счетчик
    await update.message.reply_text("Список чисел очищен.")
    # После сброса можно вернуть основное меню
    await start(update, context)

def main() -> None:
    TOKEN = "8169297356:AAF5omOWRRnRfg3yLmuDB2p9_AXHu4W-jiE"  # Замените на токен вашего бота
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))  # Обработчик команды /reset
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_number))

    # Запускаем бота
    app.run_polling()

if __name__ == '__main__':
    main()
