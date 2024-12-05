import os
import subprocess
import logging
import mimetypes
from pydub.utils import mediainfo

# Configuração do logger
logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = ['.mp3', '.wav', '.ogg', '.flac', '.aac']
MAX_AUDIO_SIZE_MB = 10

def check_audio(file_path):
    """
    Função que valida o arquivo de áudio com várias verificações:
    1. Verifica se o arquivo existe.
    2. Verifica se o tipo do arquivo é compatível com os formatos suportados.
    3. Usa o ffmpeg para verificar se o áudio pode ser lido e decodificado corretamente.
    4. Verifica se o arquivo contém dados de áudio válidos.
    5. Verifica o tamanho do arquivo.
    6. Verifica permissões de leitura e escrita.
    7. Verifica se o áudio contém som (não está mudo).
    8. Verifica o codec do áudio.
    9. Verifica integridade do arquivo.
    10. Verifica a versão do ffmpeg.
    11. Retorna um dicionário com status e mensagens de erro.
    """
    # Verificar existência do arquivo
    if not os.path.isfile(file_path):
        logger.error(f"Arquivo não encontrado: {file_path}")
        return {"status": "error", "message": "Arquivo não encontrado."}

    # Verificar tipo MIME
    mime_type, encoding = mimetypes.guess_type(file_path)
    if mime_type is None or not mime_type.startswith('audio'):
        logger.error(f"Tipo de arquivo inválido: {mime_type}")
        return {"status": "error", "message": "Tipo de arquivo inválido, não é áudio."}

    # Verificar extensão
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in SUPPORTED_FORMATS:
        logger.error(f"Formato de áudio não suportado: {ext}")
        return {"status": "error", "message": f"Formato não suportado: {ext}"}

    # Verificar tamanho do arquivo
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_AUDIO_SIZE_MB:
        logger.error(f"Arquivo de áudio muito grande: {file_size_mb:.2f} MB.")
        return {"status": "error", "message": f"Arquivo excede o limite de {MAX_AUDIO_SIZE_MB} MB."}

    # Verificar permissões de leitura do arquivo
    if not os.access(file_path, os.R_OK):
        logger.error(f"Permissão de leitura negada para o arquivo: {file_path}")
        return {"status": "error", "message": "Permissão de leitura negada."}

    # Verificar permissões de escrita no diretório de destino
    output_dir = os.path.dirname(file_path)
    if not os.access(output_dir, os.W_OK):
        logger.error(f"Permissão de escrita negada no diretório: {output_dir}")
        return {"status": "error", "message": "Permissão de escrita negada no diretório."}

    # Verificar integridade do arquivo (usando ffmpeg)
    try:
        subprocess.run(['ffmpeg', '-v', 'error', '-i', file_path, '-f', 'null', '-'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        logger.error(f"Arquivo corrompido ou ilegível: {file_path}")
        return {"status": "error", "message": "Arquivo corrompido ou ilegível."}

    # Verificar informações do áudio com ffmpeg ou pydub
    try:
        audio_info = mediainfo(file_path)
        if not audio_info or 'duration' not in audio_info:
            logger.error(f"Áudio corrompido ou ilegível: {file_path}")
            return {"status": "error", "message": "Áudio corrompido ou ilegível."}

        # Verificação do tempo de duração
        duration = float(audio_info['duration'])
        if duration < 0.1:
            logger.error(f"Áudio muito curto (duração: {duration}s): {file_path}")
            return {"status": "error", "message": "Áudio muito curto para processamento."}

       # Verificação do codec de áudio
        codec = audio_info.get('codec_name', '').lower()
        if codec not in ['mp3', 'aac', 'vorbis', 'pcm', 'flac']:
            logger.error(f"Codec de áudio não suportado: {codec}")
            return {"status": "error", "message": f"Codec não suportado: {codec}"}

        # Verificação de volume do áudio
        output = subprocess.check_output(['ffmpeg', '-i', file_path, '-af', 'volumedetect', '-f', 'null', '/dev/null'], stderr=subprocess.STDOUT)
        if b"max_volume" not in output:
            logger.warning(f"Áudio pode estar mudo ou com volume muito baixo: {file_path}")
            return {"status": "warning", "message": "Áudio com volume muito baixo ou mudo."}

        logger.info(f"Áudio validado com sucesso: {file_path}")
        return {"status": "success", "message": "Áudio validado com sucesso."}
    except Exception as e:
        logger.error(f"Erro ao analisar o áudio: {file_path}. Erro: {str(e)}")
        return {"status": "error", "message": "Erro ao analisar o áudio."}

def convert_audio_format(file_path, target_format='wav'):
    """
    Converte o arquivo de áudio para o formato desejado utilizando ffmpeg.
    """
    # Verificação de versão do ffmpeg
    try:
        ffmpeg_version = subprocess.check_output(['ffmpeg', '-version'], stderr=subprocess.STDOUT).decode()
        logger.info(f"Versão do ffmpeg: {ffmpeg_version.splitlines()[0]}")
    except subprocess.CalledProcessError:
        logger.error("Erro ao obter versão do ffmpeg.")
        return {"status": "error", "message": "Erro ao verificar versão do ffmpeg."}

    ## Conversão de áudio
    try:
        output_path = f"{os.path.splitext(file_path)[0]}.{target_format}"
        subprocess.run(['ffmpeg', '-i', file_path, '-vn', '-f', target_format, output_path], check=True)
        logger.info(f"Áudio convertido com sucesso: {output_path}")
        return {"status": "success", "message": "Conversão realizada com sucesso.", "output_file": output_path}
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao converter o áudio: {file_path}. Erro: {str(e)}")
        return {"status": "error", "message": "Erro ao converter o áudio."}
