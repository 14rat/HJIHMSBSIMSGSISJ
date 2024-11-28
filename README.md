API de Processamento de Áudio e Pesquisa na Web

Esta API permite processar áudios, transcrever o conteúdo para texto, filtrar informações para pesquisa na web e gerar respostas em áudio com base nos resultados da pesquisa. A API utiliza o Flask para gestão de requisições, Redis para cache de resultados de pesquisas e a SerpAPI para buscar informações na web.

Funcionalidades

Processamento de Áudio: Recebe arquivos de áudio (ogg, mp3 ou wav) e realiza a transcrição utilizando o serviço de reconhecimento de fala.
Pesquisa na Web: Se a transcrição contiver palavras-chave como "pesquisar" ou "buscar", a API faz uma consulta na web utilizando a SerpAPI e retorna os resultados.
Resposta em Áudio: Gera uma resposta em áudio com o número de resultados encontrados na pesquisa.
Cache de Resultados: Armazena as consultas realizadas e seus resultados em cache no Redis para otimizar requisições subsequentes.
Tecnologias Utilizadas

Flask: Framework web para Python.
Redis: Banco de dados em memória usado para cache de resultados.
SpeechRecognition: Biblioteca para reconhecimento de fala.
PyDub: Biblioteca para manipulação de arquivos de áudio.
gTTS: API do Google Text-to-Speech para gerar áudio a partir de texto.
SerpAPI: API para buscar resultados da web utilizando o Google.

Instalação

Clone o repositório:
1- git clone https://github.com/14rat/HJIHMSBSIMSGSISJ.git
cd API
2- Instale as dependências:
Utilize o arquivo requirements.txt para instalar as bibliotecas necessárias:

pip install -r requirements.txt

3- Configure o ambiente:
Crie um arquivo .env na raiz do projeto e adicione as variáveis de ambiente necessárias:

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
LOG_LEVEL=DEBUG
SERPAPI_API_KEY=sua_chave_da_serpapi
REDIS_HOST: Host do servidor Redis.
REDIS_PORT: Porta do servidor Redis (padrão: 6379).
REDIS_DB: Número do banco de dados Redis (padrão: 0).
LOG_LEVEL: Nível de log (padrão: DEBUG).
SERPAPI_API_KEY: Sua chave de API do SerpAPI

4- Inicie o servidor Flask:
Para iniciar a API, execute o seguinte comando:

python app.py
O servidor estará disponível em http://localhost:5000.