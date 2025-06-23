import logging 
import os
from datetime import datetime

# Criando diretório para os logs
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Nome do arquivo de log
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configuração correta do logging
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',  # 'w' para sobrescrever, 'a' para anexar
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
