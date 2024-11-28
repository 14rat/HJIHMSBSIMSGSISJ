import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import tempfile
import logging
import os

def transcrever_audio(arquivo_audio):
    r = sr.Recognizer()
    try:
        logging.info(f"Convertendo o áudio {arquivo_audio} para WAV...")

        # Criação de um arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav:
            audio = AudioSegment.from_file(arquivo_audio)
            audio.export(temp_wav.name, format="wav")
            logging.info(f"Áudio convertido para WAV: {temp_wav.name}")

            # Processa o áudio para transcrição
            with sr.AudioFile(temp_wav.name) as source:
                audio = r.record(source)
            texto = r.recognize_google(audio, language="pt-BR")
            logging.info(f"Texto transcrito: {texto}")
            return texto
    except sr.UnknownValueError:
        logging.error("Não consegui entender o áudio.")
        return "Não consegui entender o áudio."
    except Exception as e:
        logging.error(f"Erro ao transcrever áudio: {e}")
        return "Erro ao processar o áudio."
    finally:
        try:
            if os.path.exists(temp_wav.name):
                os.remove(temp_wav.name)
                logging.info(f"Arquivo temporário {temp_wav.name} excluído.")
        except Exception as e:
            logging.warning(f"Erro ao excluir o arquivo temporário WAV: {e}")

def gerar_audio_resposta(texto_resposta):
    try:
        logging.info(f"Gerando áudio para a resposta: {texto_resposta}")
        tts = gTTS(text=texto_resposta, lang='pt')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_mp3:
            tts.save(temp_mp3.name)
            logging.info(f"Áudio de resposta salvo em: {temp_mp3.name}")
            return temp_mp3.name
    except Exception as e:
        logging.error(f"Erro ao gerar áudio de resposta: {e}")
        return None

def validar_arquivo(audio_file):
    """Valida o tipo e tamanho do arquivo de áudio"""
    try:
        if audio_file.mimetype not in ['audio/ogg', 'audio/mpeg', 'audio/wav']:
            raise ValueError("Formato de arquivo não suportado. Envie um arquivo de áudio válido.")
        if audio_file.content_length > 10 * 1024 * 1024: 
            raise ValueError("O arquivo excede o tamanho máximo permitido de 10MB.")
        logging.info("Arquivo de áudio validado com sucesso.")
    except ValueError as e:
        logging.error(f"Erro na validação do arquivo: {e}")
        raise
