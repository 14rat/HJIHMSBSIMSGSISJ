
# API de Pesquisa com Áudio e Cache

Esta API permite processar áudios enviados, transcrevendo-os e, caso necessário, realizando uma pesquisa na web. Ela utiliza o **SerpApi** para buscar resultados na web e armazena as respostas em **Cache Redis** para otimizar as requisições subsequentes. Além disso, a API converte respostas em áudio para fornecer resultados de forma mais interativa.

## Tecnologias Usadas

- **Flask**: Framework web para a construção da API.
- **SpeechRecognition**: Biblioteca para transcrição de áudio.
- **Pydub**: Para conversão de arquivos de áudio.
- **gTTS (Google Text-to-Speech)**: Para gerar respostas em áudio.
- **Requests**: Para realizar chamadas HTTP para o SerpApi.
- **Redis**: Para cache de resultados de pesquisa.
- **Backoff**: Biblioteca para reintentar requisições falhas com backoff exponencial.

## Funcionalidades

- **Processamento de Áudio**: A API recebe arquivos de áudio, os transcreve e, se possível, realiza uma pesquisa na web sobre o conteúdo do áudio.
- **Cache de Resultados**: Armazena resultados de pesquisa no Redis para evitar consultas repetidas.
- **Geração de Resposta em Áudio**: As respostas das pesquisas são convertidas para áudio usando gTTS e retornadas como um arquivo.

## Endpoints

### `/processar_audio` [POST]

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

### PRÉ-REQUISITOS

Python 3.x: A API foi desenvolvida para rodar com Python 3.
Redis: A API utiliza Redis como cache. Você pode rodar uma instância local do Redis ou usar um serviço na nuvem como Redis Labs.
Chave da API do SerpApi: Para realizar buscas na web, é necessário ter uma chave de API do SerpApi.

### INSTALANDO DEPENDÊNCIAS

Clone o repositório:
git clone https://github.com/14rat/HJIHMSBSIMSGSISJ.git
cd API
Instalar as dependências:
pip install -r requirements.txt
Criar o arquivo .env na raiz do projeto:
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
Rodar o servidor:
python app.py
Contribuindo

### Se você deseja contribuir para o projeto, siga estas etapas:

Fork o repositório: Clique no botão "Fork" no GitHub para criar uma cópia do repositório na sua conta.
Clone o repositório forkado: Faça o clone do repositório para a sua máquina local.
Crie uma nova branch: Crie uma branch para sua funcionalidade ou correção de bug.
Faça as alterações: Implemente a funcionalidade ou correção desejada.
Faça o commit das alterações.
Envie a branch para o seu repositório remoto.
Abra um Pull Request: Vá para a página do seu repositório no GitHub e clique em "Compare & Pull Request" para enviar seu código para análise.
