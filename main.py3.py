from telegram.ext import Updater, MessageHandler, Filters
import cv2
import numpy as np
from io import BytesIO

class CartoonizerBot:
    def __init__(self, token):
        self.token = token
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        # Регистрация обработчика для фотографий
        self.dispatcher.add_handler(MessageHandler(Filters.photo, self.process_image))

    def cartoonize(self, image):
        nparr = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)

        is_success, buffer = cv2.imencode(".jpg", cartoon)
        io_buf = BytesIO(buffer)
        io_buf.name = "cartoon.jpg"

        return io_buf

    def process_image(self, update, context):
        photo = update.message.photo[-1].get_file()
        image = photo.download_as_bytearray()

        cartoon_image = self.cartoonize(image)

        context.bot.send_photo(chat_id=update.message.chat_id, photo=cartoon_image)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == "__main__":
    # Токен вашего бота
    TOKEN = '6778473784:AAFxV78Hak9XDoHVw4qg1NP15ELVeNac618'

    # Создание экземпляра класса и запуск бота
    bot = CartoonizerBot(TOKEN)
    bot.run()
