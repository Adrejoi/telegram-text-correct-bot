import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.exceptions import BotBlocked
import openai

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Welcome message
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "Hi! I'm a Grammar Correction Bot powered by ChatGPT. Send me text and I'll try to correct it. "
        "Type /cancel to stop talking to me."
    )
    await message.reply(welcome_text)

# Command to cancel or stop the bot
@dp.message_handler(commands=['cancel'])
async def cancel_handler(message: types.Message):
    await message.reply("Cancelled. Send me text again anytime you want corrections!")
    raise aiogram.utils.exceptions.CancelHandler()

# Handle text messages using ChatGPT
@dp.message_handler()
async def correct_text(message: types.Message):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Correct the following text: {message.text}",
            max_tokens=60
        )
        corrected_text = response.choices[0].text.strip()
        await message.answer(corrected_text if corrected_text else "No corrections needed.")
    except Exception as e:
        logger.error(f"Error correcting text with ChatGPT: {e}")
        await message.reply("Sorry, there was an error processing your text. Please try again.")

# Error handler for blocked bot
@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    logger.error(f"Bot was blocked by user {update.message.from_user.id}.")
    return True

# Start polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
