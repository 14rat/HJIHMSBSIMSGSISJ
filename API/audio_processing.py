import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import tempfile
import logging
import os
from typing import Union, Dict
from check_audio import check_audio

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transcrever_audio(arquivo_audio: str) -> Union[str, None]:
    """
    Função para transcrever o conteúdo de um arquivo de áudio para texto.

    Parameters:
    arquivo_audio (str): Caminho para o arquivo de áudio a ser transcrito.

    Returns:
    Union[str, None]: Texto transcrito ou mensagens de erro.
    """
    if not os.path.exists(arquivo_audio):
        logging.error(f"Arquivo de áudio não encontrado: {arquivo_audio}")
        return "Arquivo de áudio não encontrado."

    r = sr.Recognizer()
    temp_wav = None 

    try:
        logging.info(f"Iniciando o processamento do áudio: {arquivo_audio}")

        # Validar o áudio
        validation_result = check_audio(arquivo_audio)
        if validation_result['status'] != 'success':
            logging.error(f"Erro na validação do áudio: {validation_result['message']}")
            return f"Erro na validação do áudio: {validation_result['message']}"

        # Converter áudio para WAV
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav:
            try:
                audio = AudioSegment.from_file(arquivo_audio)
                audio.export(temp_wav.name, format="wav")
                logging.info(f"Áudio convertido para WAV com sucesso: {temp_wav.name}")
            except Exception as e:
                logging.error(f"Erro ao converter o áudio para WAV: {e}")
                return "Erro ao converter o áudio para o formato adequado."

        # Reconhecimento de áudio
        with sr.AudioFile(temp_wav.name) as source:
            try:
                logging.info(f"Preparando para reconhecer áudio em: {temp_wav.name}")
                audio_data = r.record(source)
                texto = r.recognize_google(audio_data, language="pt-BR")
                logging.info(f"Texto transcrito com sucesso: {texto}")
                return texto
            except sr.UnknownValueError:
                logging.error("Erro: O áudio não pôde ser transcrito.")
                return "Não consegui entender o áudio."
            except sr.RequestError as e:
                logging.error(f"Erro ao se conectar ao serviço de reconhecimento: {e}")
                return "Erro ao processar o áudio, tente novamente mais tarde."
            except Exception as e:
                logging.error(f"Erro inesperado ao transcrever o áudio: {e}")
                return "Erro ao processar o áudio."

    except Exception as e:
        logging.error(f"Erro geral no processamento do áudio: {e}")
        return "Erro ao processar o áudio."

    finally:
        # Limpeza do arquivo temporário de forma segura
        if temp_wav and os.path.exists(temp_wav.name):
            try:
                os.remove(temp_wav.name)
                logging.info(f"Arquivo temporário {temp_wav.name} excluído com sucesso.")
            except Exception as e:
                logging.warning(f"Erro ao tentar excluir o arquivo temporário WAV: {e}")


def gerar_audio_resposta(texto: str) -> Union[str, str]:
    """
    Função para gerar um arquivo de áudio a partir de um texto.

    Parameters:
    texto (str): Texto a ser convertido em áudio.

    Returns:
    Union[str, str]: Caminho para o arquivo de áudio gerado ou mensagem de erro.
    """
    if not texto:
        logging.error("Texto vazio fornecido para gerar o áudio.")
        return "Texto vazio fornecido."

    try:
        logging.info(f"Gerando áudio de resposta para o texto: {texto}")

        # Gerar o áudio de resposta
        tts = gTTS(texto, lang='pt', slow=False)
        temp_audio_file = tempfile.mktemp(suffix=".mp3")
        tts.save(temp_audio_file)

        logging.info(f"Áudio gerado com sucesso: {temp_audio_file}")
        return temp_audio_file

    except Exception as e:
        logging.error(f"Erro ao gerar áudio de resposta: {e}")
        return "Erro ao gerar áudio."


def check_audio_validity(arquivo_audio: str) -> Dict[str, str]:
    """
    Verifica se o arquivo de áudio tem o formato adequado.

    Parameters:
    arquivo_audio (str): Caminho para o arquivo de áudio.

    Returns:
    Dict[str, str]: Status da validação do arquivo de áudio.
    """
    if not arquivo_audio.endswith(('.mp3', '.wav', '.flac', '.m4a')):
        return {"status": "error", "message": "Formato de áudio inválido. Suporte para MP3, WAV, FLAC e M4A."}

    try:
        AudioSegment.from_file(arquivo_audio)
        return {"status": "success", "message": "Áudio válido."}
    except Exception as e:
        logging.error(f"Erro ao verificar a validade do áudio: {e}")
        return {"status": "error", "message": "Erro ao verificar a validade do áudio."}
