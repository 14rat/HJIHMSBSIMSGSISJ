
# API de Pesquisa com Áudio e Cache

Esta API permite processar áudios enviados, transcrevendo-os e, caso necessário, realizando uma pesquisa na web. Ela utiliza o **SerpApi** para buscar resultados na web e armazena as respostas em **DiskCache** para otimizar as requisições subsequentes. Além disso, a API converte respostas em áudio para fornecer resultados de forma mais interativa.

## Tecnologias Usadas:
**json
ffmpeg
os
logging
python-dotenv
diskcache
time
speech_recognition
pydub
gtts 
tempfile
typing
Flask
request
base64
regex
shutil
backoff
hashlib**


## Funcionalidades

- **Processamento de Áudio**: A API recebe arquivos de áudio, os transcreve e, se possível, realiza uma pesquisa na web sobre o conteúdo do áudio.
- **Cache de Resultados**: Armazena resultados de pesquisa no diskcache para evitar consultas repetidas.
- **Geração de Resposta em Áudio**: As respostas das pesquisas são convertidas para áudio usando gTTS e retornadas como um arquivo.

# Endpoints:

**`/processar_audio` [POST]**

Este endpoint recebe um arquivo de áudio e retorna a transcrição do áudio, a consulta filtrada e os resultados da pesquisa, junto com uma resposta em áudio.

#### Parâmetros
- **audio** (multipart/form-data): Arquivo de áudio para ser processado (formatos suportados: OGG, MP3, WAV).

#### Exemplo de Resposta

```json
{
  "transcricao": "Eu gostaria de pesquisar sobre inteligência artificial",
  "filtrado": "inteligência artificial",
  "resultados": [
    {
      "titulo": "Inteligência Artificial: O que é, tipos e exemplos",
      "descricao": "A inteligência artificial é um ramo da computação que cria sistemas capazes de aprender e resolver problemas.",
      "link": "https://example.com/artigo1"
    },
    {
      "titulo": "O futuro da Inteligência Artificial",
      "descricao": "Estudo sobre as tendências e desenvolvimentos futuros na área de IA.",
      "link": "https://example.com/artigo2"
    },
    {
      "titulo": "Introdução à Inteligência Artificial",
      "descricao": "Guia inicial para entender a IA, suas aplicações e desafios.",
      "link": "https://example.com/artigo3"
    }
  ],
  "audio": "data:audio/mp3;base64,..."
}
```

# PRÉ-REQUISITOS

**Python 3.x**: A API foi desenvolvida para rodar com Python 3.
**Chave da API do SerpApi**: Para realizar buscas na web, é necessário ter uma chave de API do SerpApi.

### INSTALANDO DEPENDÊNCIAS

Clone o repositório:
git clone https://github.com/14rat/HJIHMSBSIMSGSISJ.git
cd API

# Instalar as dependências:
pip install -r requirements.txt

# Criar o arquivo .env na raiz do projeto:

# Nível de log
LOG_LEVEL=DEBUG

# Chave da API do SerpApi
SERPAPI_API_KEY=sua_chave_de_api_serpapi

# Configurações do Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Configurações do Flask (opcional, dependendo do seu uso)
FLASK_ENV=development

# Timeout da requisição para a SERPAPI (em segundos)
SERPAPI_SEARCH_TIMEOUT=10  # Timeout de 10 segundos

# Expiração do cache (em segundos)
CACHE_EXPIRATION=3600  # 1 hora
# Rodar o servidor:
python app.py

# Exemplos de Resultados de Erro:
**Erro de Validação de Áudio**
```json
{
  "error": "Arquivo não encontrado."
}
```
**Erro ao Processar o Áudio**
```json
{
  "error": "Ocorreu um erro ao processar o áudio. Tente novamente mais tarde."
}
```