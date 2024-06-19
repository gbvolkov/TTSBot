import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import TELEGRAM_BOT_TOKEN
from voice_gen import get_all_voices, generate_audio

# Initialize the bot with your token
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Store user data
user_data = {}

# Handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    voices = get_all_voices()
    user_data[message.chat.id] = {'voices': voices, 'selected_voice': None}
    
    markup = ReplyKeyboardMarkup(row_width=2)
    for voice in voices:
        markup.add(KeyboardButton(voice['name']))
    
    bot.send_message(message.chat.id, "Привет! Я бот для создания озвучки! Выбери голос, который будет использоваться при создании озвучки.", reply_markup=markup)

# Handle text messages for voice selection and text input
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    if user_id in user_data and user_data[user_id]['selected_voice'] is None:
        selected_voice = next((voice for voice in user_data[user_id]['voices'] if voice['name'] == message.text), None)
        if selected_voice:
            user_data[user_id]['selected_voice'] = selected_voice
            bot.send_message(user_id, f"Вы выбрали голос: {selected_voice['name']}. Теперь введите текст для озвучки.")
        else:
            bot.send_message(user_id, "Пожалуйста, выберите голос с клавиатуры.")
    else:
        if user_id in user_data and user_data[user_id]['selected_voice']:
            voice_id = user_data[user_id]['selected_voice']['id']
            audio = generate_audio(message.text, voice_id)
            #with open(audio_file, 'rb') as audio:
            bot.send_audio(user_id, audio)
            bot.send_voice(user_id, audio)

# Start polling for new messages
if __name__ == "__main__":
    bot.polling(none_stop=True)
