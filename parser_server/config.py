from dotenv import load_dotenv
import os
from tools.logger import setup_logger

load_dotenv()

# Загрузка URL сервера
SERVER_URL = os.getenv('SERVER_URL')
GLOBAL_SERVER_URL = os.getenv('GLOBAL_SERVER_URL')

# Определение URL API сервера
SERVER_API_URL = GLOBAL_SERVER_URL if GLOBAL_SERVER_URL else SERVER_URL

# Загрузка порта сервера
SERVER_PORT = os.getenv('SERVER_PORT')
GLOBAL_SERVER_PORT = os.getenv('GLOBAL_SERVER_PORT')

# Определение порта API сервера
SERVER_API_PORT = GLOBAL_SERVER_PORT if GLOBAL_SERVER_PORT else SERVER_PORT

# Логгеры для различных компонентов
server_logger = setup_logger("server", "server")
scrapper_logger = setup_logger("scrapper", "scrapper")
rbk_logger = setup_logger("rbk", "src/rbk")
lenta_logger = setup_logger("lenta", "src/lenta")
ria_logger = setup_logger("ria", "src/ria")
gazeta_logger = setup_logger("gazeta", "src/gazeta")
