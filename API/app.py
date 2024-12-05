from flask import Flask, request, jsonify
import logging
from dotenv import load_dotenv
import os
import tempfile
import base64
from audio_processing import transcrever_audio, gerar_audio_resposta
from web_search import pesquisar_na_web
from cache.cache_manager import obter_cache, armazenar_cache
import re
import shutil
from check_audio import check_audio, convert_audio_format

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()
logging.basicConfig(filename='logs/api.log', level=getattr(logging, log_level), format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializa o Flask
app = Flask(__name__)

# Função de filtragem de comandos de pesquisa
def filtrar_por_palavra_chave(texto):
    comandos_chave = [
        r"pesquisar\s*(.*)",   
        r"buscar\s*(.*)",       
        r"me\s*encontre\s*(.*)", 
        r"faça\s*uma\s*pesquisa\s*sobre\s*(.*)",  
        r"procure\s*(.*)",      
        r"encontre\s*(.*)",     
        r"encontre\s*informações\s*sobre\s*(.*)", 
        r"quero\s*ver\s*(.*)",  
    ]
    for comando in comandos_chave:
        match = re.search(comando, texto, re.IGNORECASE)
        if match:
            consulta = match.group(1).strip()
            logging.info(f"Comando de pesquisa identificado: {consulta}")
            return consulta
    logging.info(f"Texto filtrado sem comando específico: {texto.strip()}")
    return texto.strip()

@app.route('/processar_audio', methods=['POST'])
def processar_audio():
    if 'audio' not in request.files:
        logging.warning("Nenhum áudio enviado na requisição.")
        return jsonify({"error": "Nenhum áudio enviado."}), 400

    try:
        # Validação do arquivo de áudio
        audio_file = request.files['audio']
        temp_audio_path = tempfile.mktemp(suffix='.ogg')
        audio_file.save(temp_audio_path)
        validation_result = check_audio(temp_audio_path)
        if validation_result['status'] != 'success':
            logging.error(f"Erro na validação do áudio: {validation_result['message']}")
            return jsonify({"error": validation_result['message']}), 400

        # Caso o formato do áudio não seja WAV, converte para WAV
        if validation_result['message'] != "Áudio validado com sucesso.":
            conversion_result = convert_audio_format(temp_audio_path, target_format='wav')
            if conversion_result['status'] != 'success':
                logging.error(f"Erro ao converter o áudio para WAV: {conversion_result['message']}")
                return jsonify({"error": conversion_result['message']}), 400
            temp_audio_path = conversion_result['output_file']

        # Transcrição do áudio para texto
        texto_transcrito = transcrever_audio(temp_audio_path)
        if texto_transcrito == "Não consegui entender o áudio.":
            logging.error("Não consegui transcrever o áudio, possivelmente com baixa qualidade.")
            return jsonify({"error": "Não consegui transcrever o áudio. Tente um áudio mais claro."}), 400

        # Filtragem do texto transcrito para identificar comando de pesquisa
        texto_filtrado = filtrar_por_palavra_chave(texto_transcrito)
        if not texto_filtrado:
            logging.warning(f"Texto transcrito não contém um comando de pesquisa válido: {texto_transcrito}")
            return jsonify({"message": "Não foi possível interpretar a consulta a partir da transcrição."}), 400

        logging.info(f"Consulta filtrada: {texto_filtrado}")
        query = texto_filtrado.strip()

        # Tentativa de obter resultados do cache
        try:
            cache_resultados = obter_cache(query)
            if cache_resultados:
                logging.info(f"Resultados encontrados no cache para a consulta: {query}")
                resultados_pesquisa = cache_resultados
            else:
                logging.info(f"Buscando resultados para a consulta: {query}")
                resultados_pesquisa = pesquisar_na_web(query)
                if resultados_pesquisa:
                    # Armazenando os resultados no cache
                    armazenar_cache(query, resultados_pesquisa)
                else:
                    logging.warning(f"Sem resultados encontrados para a pesquisa: {query}")
                    return jsonify({"message": "Nenhum resultado relevante encontrado."}), 404
        except Exception as e:
            logging.error(f"Erro ao acessar o cache: {e}")
            return jsonify({"error": "Erro ao acessar o cache."}), 500

        # Geração do áudio de resposta baseado nos resultados encontrados
        texto_audio = f"Sua pesquisa sobre {query} resultou em {len(resultados_pesquisa)} resultados encontrados."
        arquivo_audio_resposta = gerar_audio_resposta(texto_audio)

        # Leitura e codificação do arquivo de áudio gerado para retorno na resposta
        with open(arquivo_audio_resposta, 'rb') as audio_file:
            audio_content = base64.b64encode(audio_file.read()).decode('utf-8')

        # Retorno dos dados
        return jsonify({
            'transcricao': texto_transcrito,
            'filtrado': texto_filtrado,
            'resultados': resultados_pesquisa,
            'audio': audio_content
        }), 200

    except ValueError as e:
        logging.error(f"Erro de validação: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Erro inesperado ao processar o áudio: {e}")
        return jsonify({"error": "Ocorreu um erro ao processar o áudio. Tente novamente mais tarde."}), 500
    finally:
        # Limpeza dos arquivos temporários após o processamento
        try:
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                logging.info(f"Arquivo temporário {temp_audio_path} removido com sucesso.")
        except Exception as e:
            logging.warning(f"Erro ao tentar remover o arquivo temporário: {e}")

if __name__ == "__main__":
    app.run(debug=True)
