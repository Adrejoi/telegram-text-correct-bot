import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.exceptions import BotBlocked
from textblob import TextBlob

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Welcome message
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "Hi! I'm a Grammar Correction Bot. Send me text and I'll try to correct it. "
        "Type /cancel to stop talking to me."
    )
    await message.reply(welcome_text)

# Command to cancel or stop the bot
@dp.message_handler(commands=['cancel'])
async def cancel_handler(message: types.Message):
    await message.reply("Cancelled. Send me text again anytime you want corrections!")
    raise aiogram.utils.exceptions.CancelHandler()

# Handle text messages
@dp.message_handler()
async def correct_text(message: types.Message):
    try:
        corrected_text = TextBlob(message.text)
        await message.answer(str(corrected_text.correct()))
    except Exception as e:
        logger.error(f"Error correcting text: {e}")
        await message.reply("Sorry, I couldn't process your text. Please try again.")

# Error handler for blocked bot
@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    logger.error(f"Bot was blocked by user {update.message.from_user.id}.")
    return True

# Start polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
