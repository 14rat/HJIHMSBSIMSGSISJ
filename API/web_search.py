import requests
import os
import logging
from dotenv import load_dotenv

#CARREGA AS CHAVES DA API
load_dotenv()

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
SERPAPI_SEARCH_URL = "https://serpapi.com/search"

def pesquisar_na_web(query):
    try:
        params = {
            'q': query,
            'api_key': SERPAPI_API_KEY,
            'engine': 'google',
        }

        response = requests.get(SERPAPI_SEARCH_URL, params=params)
        response.raise_for_status()

        resultados = response.json()

        if 'organic_results' in resultados:
            resposta = []
            for item in resultados['organic_results'][:3]:
                titulo = item.get('title', 'Sem título')
                descricao = item.get('snippet', 'Sem descrição')
                link = item.get('link', 'Sem link')
                resposta.append({
                    'titulo': titulo,
                    'descricao': descricao,
                    'link': link
                })
            return resposta
        else:
            logging.warning(f"Nenhum resultado encontrado para a consulta: {query}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de requisição ao buscar na web com SerpApi: {e}")
        return None
    except Exception as e:
        logging.error(f"Erro desconhecido ao buscar na web: {e}")
        return None
