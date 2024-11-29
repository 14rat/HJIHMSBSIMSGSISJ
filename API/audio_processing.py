import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import tempfile
import logging
import os
import io

def transcrever_audio(arquivo_audio):
    r = sr.Recognizer()
    temp_wav = None  
    try:
        logging.info(f"Iniciando o processamento do áudio: {arquivo_audio}")

        # Verificar se o arquivo realmente existe
        if not os.path.exists(arquivo_audio):
            logging.error(f"O arquivo de áudio não existe: {arquivo_audio}")
            return "Arquivo de áudio não encontrado."

        # Convertemos o áudio para WAV
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav:
            try:
                audio = AudioSegment.from_file(arquivo_audio)
                audio.export(temp_wav.name, format="wav")
                logging.info(f"Áudio convertido para WAV com sucesso: {temp_wav.name}")
            except Exception as e:
                logging.error(f"Erro ao converter o áudio para WAV: {e}")
                return "Erro ao converter o áudio para o formato adequado."

        # Realizar o reconhecimento de áudio com o SpeechRecognition
        try:
            with sr.AudioFile(temp_wav.name) as source:
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
    finally:
        # Garantir que o arquivo temporário seja removido após o uso
        if temp_wav and os.path.exists(temp_wav.name):
            try:
                os.remove(temp_wav.name)
                logging.info(f"Arquivo temporário {temp_wav.name} excluído com sucesso.")
            except Exception as e:
                logging.warning(f"Erro ao tentar excluir o arquivo temporário WAV: {e}")


def gerar_audio_resposta(texto_resposta):
    try:
        logging.info(f"Iniciando a geração de áudio para a resposta: {texto_resposta}")

        if not texto_resposta or len(texto_resposta.strip()) == 0:
            logging.error("Texto da resposta vazio ou inválido.")
            return None

        tts = gTTS(text=texto_resposta, lang='pt')

        # Gerar o arquivo de áudio temporário MP3
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_mp3:
            tts.save(temp_mp3.name)
            logging.info(f"Áudio de resposta gerado e salvo em: {temp_mp3.name}")
            return temp_mp3.name
    except Exception as e:
        logging.error(f"Erro ao gerar áudio de resposta: {e}")
        return None


def validar_arquivo(audio_file):
    try:
        formatos_validos = ['audio/ogg', 'audio/mpeg', 'audio/wav']
        if audio_file.mimetype not in formatos_validos:
            raise ValueError(f"Formato de arquivo não suportado. Formatos válidos são: {', '.join(formatos_validos)}.")

        if audio_file.content_length > 10 * 1024 * 1024: 
            raise ValueError("O arquivo excede o tamanho máximo permitido de 10MB.")

        logging.info(f"Arquivo de áudio validado com sucesso: {audio_file.filename}")
    except ValueError as e:
        logging.error(f"Erro na validação do arquivo {audio_file.filename}: {e}")
        raise  
    except Exception as e:
        logging.error(f"Erro desconhecido ao validar o arquivo {audio_file.filename}: {e}")
        raise


