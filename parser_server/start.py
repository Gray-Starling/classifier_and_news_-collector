import time
import threading
import asyncio
from flask import Flask
from scrapper import main as scrapper_main
from config import server_logger, SERVER_API_URL, SERVER_API_PORT

app = Flask(__name__)
HOST = SERVER_API_URL
PORT = SERVER_API_PORT

def run_scrapper_periodically():
    """
    Функция для запуска в потоке, которая регулярно выполняет скрапинг новостей.
    
    В бесконечном цикле функция выполняет скрапинг новостей, используя асинхронную функцию
    `scrapper_main()`. Логирует статус выполнения и любые ошибки при выполнении. После каждого 
    выполнения ждет 10 минут перед следующим запуском.

    Логирование осуществляется через `server_logger`, который должен быть настроен перед 
    использованием данного кода.

    Raises:
        Может возникать любое исключение, которое может выбросить функция `scrapper_main()`.
    """
    while True:
        try: 
            server_logger.info("News scrapper is running")
            asyncio.run(scrapper_main())
            server_logger.info("News scrapper finished")
        except Exception as e:
            server_logger.error(f"Error running scrapper: {e}")
        server_logger.info("Sleeping for 10 minutes. \n")
        time.sleep(600)

# @app.route('/api/v1/news')
# def index():
#     return jsonify({"message": "News scrapper is running"}), 200

if __name__ == "__main__":
    scrapper_thread = threading.Thread(target=run_scrapper_periodically)
    scrapper_thread.daemon = True
    scrapper_thread.start()

    app.run(host=HOST, port=PORT)