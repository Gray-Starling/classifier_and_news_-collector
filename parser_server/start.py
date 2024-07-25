import time
import threading
import asyncio
from flask import Flask, send_file
from scrapper import main as scrapper_main
from config import server_logger, SERVER_API_URL, SERVER_API_PORT

app = Flask(__name__)
HOST = SERVER_API_URL
PORT = SERVER_API_PORT

def run_scrapper_periodically():
   
    while True:
        try: 
            server_logger.info("News scrapper is running")
            asyncio.run(scrapper_main())
            server_logger.info("News scrapper finished")
        except Exception as e:
            server_logger.error(f"Error running scrapper: {e}")
        server_logger.info("Sleeping for 10 minutes. \n")
        time.sleep(600)

@app.route('/api/v1/news')
def index():
    file_path = "news.csv"  # Путь к вашему файлу
    return send_file(file_path, as_attachment=True)  # Отправка файла как вложения

if __name__ == "__main__":
    scrapper_thread = threading.Thread(target=run_scrapper_periodically)
    scrapper_thread.daemon = True
    scrapper_thread.start()

    app.run(host=HOST, port=PORT)