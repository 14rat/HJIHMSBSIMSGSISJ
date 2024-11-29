import json
import os
import logging
from dotenv import load_dotenv
import diskcache
from time import time
from logging.handlers import RotatingFileHandler

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do diretório de cache e timeout
CACHE_DIR = os.getenv('CACHE_DIR', 'API/cache')
CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 3600))

# Configuração do diretório de logs e arquivo de log
LOG_DIR = os.getenv('LOG_DIR', 'API/logs')  
LOG_FILE = os.path.join(LOG_DIR, 'api.log')

# Garantir que os diretórios de cache e log existam
for directory in [CACHE_DIR, LOG_DIR]:
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
            logging.info(f"Diretório criado em: {directory}")
        except Exception as e:
            logging.error(f"Erro ao criar o diretório {directory}: {e}")
            raise

# Configuração do logging
log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, log_level))

# Rotacionando arquivos de log
handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=3)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())  

# Criando o cache com diskcache
try:
    cache = diskcache.Cache(CACHE_DIR)
    logger.info(f"Cache inicializado com sucesso em {CACHE_DIR}.")
except Exception as e:
    logger.error(f"Erro ao inicializar o cache em {CACHE_DIR}: {e}")
    raise

# Função para obter cache
def obter_cache(query):
    try:
        logger.debug(f"Buscando cache para a consulta: {query}")
        cached_result = cache.get(query)
        if cached_result:
            logger.info(f"Cache encontrado para a consulta: {query}")
            return json.loads(cached_result)
        else:
            logger.info(f"Nenhum cache encontrado para a consulta: {query}")
            return None
    except diskcache.CacheError as e:
        logger.error(f"Erro ao acessar o cache para a consulta {query}: {e}")
        return None

# Função para armazenar cache
def armazenar_cache(query, resultados, expira_em_segundos=CACHE_TIMEOUT):
    try:
        logger.debug(f"Armazenando resultados no cache para a consulta: {query}")

        if not resultados:
            logger.warning(f"Tentativa de armazenar resultados vazios para a consulta {query}. Cache não será atualizado.")
            return

        # Garantir que os resultados sejam serializáveis
        try:
            resultados_json = json.dumps(resultados)
        except (TypeError, ValueError) as e:
            logger.error(f"Erro ao serializar os resultados para a consulta {query}: {e}")
            return

        # Armazenando no cache
        cache.set(query, resultados_json, expire=expira_em_segundos)
        logger.info(f"Resultados armazenados com sucesso no cache para a consulta: {query}. Expiração em {expira_em_segundos} segundos.")
    except diskcache.CacheError as e:
        logger.error(f"Erro ao tentar armazenar resultados no cache para a consulta {query}: {e}")

# Função para limpar o cache
def limpar_cache():
    try:
        logger.info("Iniciando limpeza do cache...")
        cache.clear()
        logger.info("Cache limpo com sucesso.")
    except diskcache.CacheError as e:
        logger.error(f"Erro ao tentar limpar o cache: {e}")

# Função de verificação da saúde do cache
def verificar_conexao():
    try:
        test_key = 'test_key'
        test_value = 'test_value'
        cache.set(test_key, test_value, expire=60)
        if cache.get(test_key) == test_value:
            logger.info(f"Cache está operacional em {CACHE_DIR}.")
            return True
        else:
            logger.error("Falha ao verificar a escrita e leitura no cache.")
            return False
    except diskcache.CacheError as e:
        logger.error(f"Erro ao verificar conexão com o cache: {e}")
        return False

# Função para medir a performance do cache
def medir_performance(iteracoes=100):
    start_time = time()

    for _ in range(iteracoes):
        cache.set("performance_test", "OK", expire=60)
        cache.get("performance_test")

    end_time = time()
    logger.info(f"Performance do cache: {end_time - start_time:.6f} segundos para {iteracoes} operações de leitura e escrita.")
