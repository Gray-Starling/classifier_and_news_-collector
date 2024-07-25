from dotenv import load_dotenv
import os
# from tools.logger import setup_logger

load_dotenv()

# Загрузка URL сервера
NEWS_DATA_API_URL = os.getenv('NEWS_DATA_API_URL')
GLOBAL_NEWS_DATA_API_URL = os.getenv('GLOBAL_NEWS_DATA_API_URL')

# Определение URL API сервера
NEWS_DATA_API = GLOBAL_NEWS_DATA_API_URL if GLOBAL_NEWS_DATA_API_URL else NEWS_DATA_API_URL

# Загрузка порта сервера
# SERVER_PORT = os.getenv('SERVER_PORT')
# GLOBAL_SERVER_PORT = os.getenv('GLOBAL_SERVER_PORT')

# # Определение порта API сервера
# SERVER_API_PORT = GLOBAL_SERVER_PORT if GLOBAL_SERVER_PORT else SERVER_PORT

