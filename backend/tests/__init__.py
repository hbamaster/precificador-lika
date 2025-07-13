import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

# Configuração do diretório de logs
LOG_DIR = "logs"
Path(LOG_DIR).mkdir(exist_ok=True)  # Cria o diretório se não existir

# Configuração básica do logger
def setup_logging():
    """Configura o sistema de logging da aplicação"""
    
    # Formato padrão
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo (com rotação)
    file_handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, 'api.log'),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # Configuração global
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],
    )

    # Desabilita logs muito verbosos de bibliotecas
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)

# Chama a configuração quando o módulo é importado
setup_logging()

# Logger raiz para ser importado em outros módulos
logger = logging.getLogger(__name__)
logger.info("Configuração de logging inicializada")