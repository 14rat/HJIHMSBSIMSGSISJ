import redis
import json
import os
import logging

# Configuração do Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Conexão com Redis
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def obter_cache(query):
    """Obtém os dados do cache do Redis"""
    try:
        cached_result = r.get(query)
        if cached_result:
            return json.loads(cached_result)
        return None
    except redis.RedisError as e:
        logging.error(f"Erro ao acessar o cache Redis: {e}")
        return None

def armazenar_cache(query, resultados):
    """Armazena dados no cache do Redis"""
    try:
        r.set(query, json.dumps(resultados), ex=3600)  # Cache por 1 hora
    except redis.RedisError as e:
        logging.error(f"Erro ao armazenar no cache Redis: {e}")
