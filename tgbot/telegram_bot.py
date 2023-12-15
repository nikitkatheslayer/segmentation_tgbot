import os
import telebot
from detection.segment_func import SegmentImage
from config import TOKEN

seg = SegmentImage()
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):

    mess = f"<b>{message.from_user.first_name}</b>, отправь мне фотографию, чтобы я распознал на нем человека"
    bot.send_message(message.chat.id, mess, parse_mode="html")

@bot.message_handler(content_types=["photo"])
def get_user_photo(message):
    global src
    try:
        bot.send_message(message.chat.id, "Обрабатываю изображение...", parse_mode="html")

        file_photo = bot.get_file(message.photo[-1].file_id)
        file_name, file_extension = os.path.splitext(file_photo.file_path)

        downloaded_file_photo = bot.download_file(file_photo.file_path)

        try:
            src = "image/" + message.photo[-1].file_id + file_extension
            with open(src, "wb") as new_file:
                new_file.write(downloaded_file_photo)
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка при записи файла: {e}", parse_mode="html")

        if not os.path.exists("image"):
            try:
                os.makedirs("image")
            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка при создании директории: {e}", parse_mode="html")

        try:
            seg.object_detection_on_an_image(src)

            bot.send_message(message.chat.id, "Отправляю вам изображение...", parse_mode="html")
            detected_file_photo_path = "image/" + message.photo[-1].file_id + "_detected_faces.jpg"
            detected_file_photo = open(detected_file_photo_path, "rb")
            bot.send_photo(message.chat.id, detected_file_photo)

            bot.send_message(message.chat.id, "Можешь отправить еще одно изображение", parse_mode="html")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка при обработке изображения: {e}", parse_mode="html")

    except ValueError as e:
        print(f"Произошло исключение типа ValueError: {e}")

@bot.message_handler(content_types=["file", "text", "voice", "document", "video"])
def handl_errors(message):
    bot.send_message(message.chat.id, "Отправьте фото или видео")

bot.polling(none_stop=True)