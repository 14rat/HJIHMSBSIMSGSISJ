import redis
import json
import os
import logging
from dotenv import load_dotenv
from redis.exceptions import RedisError, ConnectionError, TimeoutError

# Carregar variáveis de ambiente
load_dotenv()

# Configuração das variáveis de Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_TIMEOUT = int(os.getenv('REDIS_TIMEOUT', 5))  

# Configurar o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Tentando conectar ao Redis
try:
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True, socket_timeout=REDIS_TIMEOUT)
    r.ping()
    logging.info(f"Conectado com sucesso ao Redis em {REDIS_HOST}:{REDIS_PORT}")
except (ConnectionError, TimeoutError) as e:
    logging.error(f"Erro ao conectar ao Redis: {e}")
    raise Exception("Falha ao conectar ao Redis. Verifique sua configuração e conexão.")
except RedisError as e:
    logging.error(f"Erro desconhecido ao conectar ao Redis: {e}")
    raise Exception("Erro inesperado ao tentar conectar ao Redis.")

# Função para obter cache
def obter_cache(query):
    try:
        logging.debug(f"Buscando cache para a consulta: {query}")
        cached_result = r.get(query)
        if cached_result:
            logging.info(f"Cache encontrado para a consulta: {query}")
            return json.loads(cached_result)
        else:
            logging.info(f"Nenhum cache encontrado para a consulta: {query}")
            return None
    except RedisError as e:
        logging.error(f"Erro ao acessar o cache Redis para a consulta {query}: {e}")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado ao acessar o cache para a consulta {query}: {e}")
        return None

# Função para armazenar cache
def armazenar_cache(query, resultados, expira_em_segundos=3600):
    try:
        logging.debug(f"Armazenando resultados no cache para a consulta: {query}")
        if not resultados:
            logging.warning(f"Tentativa de armazenar resultados vazios para a consulta {query}. Cache não será atualizado.")
            return

        # Garantir que os resultados são serializáveis
        resultados_json = json.dumps(resultados)

        r.set(query, resultados_json, ex=expira_em_segundos) 
        logging.info(f"Resultados armazenados com sucesso no cache para a consulta: {query}. Expiração em {expira_em_segundos} segundos.")
    except (RedisError, TimeoutError) as e:
        logging.error(f"Erro ao armazenar no cache Redis para a consulta {query}: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado ao tentar armazenar resultados no cache para a consulta {query}: {e}")

# Função para limpar o cache
def limpar_cache():
    try:
        logging.info("Iniciando limpeza do cache...")
        r.flushdb() 
        logging.info("Cache limpo com sucesso.")
    except (RedisError, TimeoutError) as e:
        logging.error(f"Erro ao tentar limpar o cache Redis: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado ao limpar o cache: {e}")

# Função de verificação da saúde do Redis
def verificar_conexao():
    try:
        r.ping()
        logging.info(f"Redis está operacional em {REDIS_HOST}:{REDIS_PORT}.")
        return True
    except RedisError as e:
        logging.error(f"Erro ao verificar conexão com Redis: {e}")
        return False
