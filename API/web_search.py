import os
import requests
import logging
import time
import backoff
import hashlib
import json
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError
from dotenv import load_dotenv  

# Carregar as variáveis do arquivo .env
load_dotenv()

# Ler a chave de API do arquivo .env
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')  
SERPAPI_SEARCH_URL = 'https://serpapi.com/search'
API_TIMEOUT = 10  
MAX_RETRIES = 3  

# Função de retry com backoff exponencial
@backoff.on_exception(backoff.expo, (RequestException, ConnectionError, Timeout), max_tries=MAX_RETRIES, jitter=None)
def request_func(params):
    """
    Função que realiza a requisição para a API do SERPAPI.
    O backoff é aplicado para erros de rede, como timeout e conexão.
    """
    logging.debug(f"Enviando requisição para a API com parâmetros: {params}")
    response = requests.get(SERPAPI_SEARCH_URL, params=params, timeout=API_TIMEOUT)
    response.raise_for_status()
    return response.json()

def pesquisar_na_web(query):
    """
    Função de busca na web utilizando a API do SERPAPI.
    Realiza o request, com tratamento de erros e logging robusto.
    """
    try:
        logging.info(f"Iniciando pesquisa na web para a consulta: '{query}'")

        # Sanitizar a consulta para garantir que ela está formatada corretamente
        query = query.strip()
        if not query:
            logging.warning("Consulta vazia fornecida. Nenhum resultado será retornado.")
            return None

        # Gerar chave de cache baseada na consulta para evitar buscas duplicadas
        query_hash = hashlib.md5(query.encode('utf-8')).hexdigest()
        cache_file = f"cache_{query_hash}.json"

        # Verificar se já temos cache para esta consulta
        if os.path.exists(cache_file):
            logging.info(f"Utilizando cache para a consulta: '{query}'")
            with open(cache_file, 'r') as cache_f:
                cached_data = json.load(cache_f)
                return cached_data

        params = {
            'q': query,
            'api_key': SERPAPI_API_KEY,
            'engine': 'google',
        }

        # Realizar a requisição à API com backoff em caso de falhas temporárias
        try:
            resultados = request_func(params)

            
            if 'organic_results' not in resultados:
                logging.warning(f"Nenhum resultado encontrado na resposta da API para a consulta: {query}")
                return None


            resposta = [{
                'titulo': item.get('title', 'Sem título'),
                'descricao': item.get('snippet', 'Sem descrição'),
                'link': item.get('link', 'Sem link')
            } for item in resultados['organic_results'][:3]]

            logging.info(f"Consulta '{query}' retornou {len(resposta)} resultados.")

            # Salvar resultados no cache para otimizar futuras requisições
            with open(cache_file, 'w') as cache_f:
                json.dump(resposta, cache_f)
            logging.info(f"Resultados armazenados em cache para a consulta: '{query}'")

            return resposta

        except (RequestException, HTTPError, Timeout, ConnectionError) as e:
            logging.error(f"Erro ao realizar a requisição para a consulta '{query}': {e}")
            return None

    except Exception as e:
        logging.error(f"Erro inesperado ao buscar na web para a consulta '{query}': {e}")
        return None
