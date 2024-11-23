import redis
import json
import os

# Configuração do Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = os.getenv('REDIS_DB', 0)

r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def obter_cache(query):
    cached_result = r.get(query)
    if cached_result:
        return json.loads(cached_result)
    return None


def armazenar_cache(query, resultados):
    r.set(query, json.dumps(resultados), ex=3600) 
