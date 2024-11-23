from flask import Flask, request, jsonify
import logging
from dotenv import load_dotenv
from audio_processing import transcrever_audio, filtrar_texto, gerar_audio_resposta, validar_arquivo
from web_search import pesquisar_na_web
from cache.cache_manager import obter_cache, armazenar_cache
import os
import tempfile
import base64

# Carregar variáveis de ambiente
load_dotenv()

# Configura o logging
log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()
logging.basicConfig(filename='logs/api.log', level=getattr(logging, log_level), format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializa o Flask
app = Flask(__name__)

# Função para identificar palavras-chave 
def filtrar_por_palavra_chave(texto):
    palavras_chaves = ["pesquisar", "buscar"]
    for palavra in palavras_chaves:
        posicao = texto.lower().find(palavra)
        if posicao != -1:
            return texto[posicao + len(palavra):].strip()
    return texto  

@app.route('/processar_audio', methods=['POST'])
def processar_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "Nenhum áudio enviado."}), 400

    try:
        audio_file = request.files['audio']
        validar_arquivo(audio_file) 
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_audio:
            audio_file.save(temp_audio.name)
            logging.info(f"Áudio recebido e salvo em {temp_audio.name}.")

            # Transcrição do áudio
            texto_transcrito = transcrever_audio(temp_audio.name)
            if texto_transcrito == "Não consegui entender o áudio.":
                return jsonify({"error": "Não consegui transcrever o áudio. Tente um áudio mais claro."}), 400

            texto_filtrado = filtrar_por_palavra_chave(texto_transcrito)

           
            if "pesquisar" in texto_filtrado.lower() or "buscar" in texto_filtrado.lower():
                query = texto_filtrado.replace("pesquisar", "").replace("buscar", "").strip()

               
                cache_resultados = obter_cache(query)
                if cache_resultados:
                    logging.info(f"Resultados encontrados no cache para a consulta: {query}")
                    resultados_pesquisa = cache_resultados
                else:
                    resultados_pesquisa = pesquisar_na_web(query)
                    if resultados_pesquisa:
                        armazenar_cache(query, resultados_pesquisa)
                    else:
                        logging.warning(f"Sem resultados para a pesquisa: {query}")
                        return jsonify({"message": "Nenhum resultado relevante encontrado."}), 404

               
                texto_audio = f"Sua pesquisa sobre {query} resultou em {len(resultados_pesquisa)} resultados encontrados."
                arquivo_audio_resposta = gerar_audio_resposta(texto_audio)

                with open(arquivo_audio_resposta, 'rb') as audio_file:
                    audio_content = base64.b64encode(audio_file.read()).decode('utf-8')

                return jsonify({
                    'transcricao': texto_transcrito,
                    'filtrado': texto_filtrado,
                    'resultados': resultados_pesquisa,
                    'audio': audio_content
                }), 200

            return jsonify({
                'transcricao': texto_transcrito,
                'filtrado': texto_filtrado
            }), 200

    except ValueError as e:
        logging.error(f"Erro de validação: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Erro ao processar o áudio: {e}")
        return jsonify({"error": "Ocorreu um erro ao processar o áudio. Tente novamente mais tarde."}), 500
    finally:
        try:
            if 'temp_audio' in locals():
                os.remove(temp_audio.name)
                logging.info(f"Arquivo temporário {temp_audio.name} removido com sucesso.")
        except Exception as e:
            logging.warning(f"Erro ao remover o arquivo temporário: {e}")

if __name__ == "__main__":
    app.run(debug=True)
