API de Processamento de Áudio e Pesquisa na Web

Esta API permite que você envie arquivos de áudio, obtenha transcrições de texto, realize pesquisas na web baseadas em palavras-chave transcritas, e receba respostas em áudio com base nos resultados encontrados. Ela utiliza Flask, Redis para cache, SerpAPI para busca na web e Google Text-to-Speech (gTTS) para gerar áudio.

Funcionalidades

Transcrição de Áudio: Converte áudio em texto utilizando reconhecimento de fala.
Pesquisa na Web: Realiza pesquisas na web com base no conteúdo transcrito do áudio.
Resposta em Áudio: Gera uma resposta de áudio contendo o número de resultados encontrados para a pesquisa.
Cache de Resultados: Utiliza Redis para armazenar os resultados das consultas e evitar requisições repetidas à web.
Tecnologias Utilizadas

Flask: Framework web para Python.
Redis: Banco de dados em memória utilizado para cache.
SpeechRecognition: Biblioteca para reconhecimento de fala.
PyDub: Biblioteca para manipulação de áudio.
gTTS: API do Google Text-to-Speech para conversão de texto em fala.
SerpAPI: API para realizar buscas na web utilizando o Google.
Pré-Requisitos

Python 3.x (certifique-se de ter o Python 3 instalado no seu ambiente).
Redis (instalado e em execução localmente ou em um servidor remoto).
Instalação

1. Clone o Repositório
Clone o repositório para o seu ambiente local:

git clone https://github.com/seu-usuario/sua-api.git
cd sua-api
2. Instale as Dependências
Instale todas as dependências necessárias utilizando o arquivo requirements.txt:

pip install -r requirements.txt
3. Configuração das Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis de ambiente:

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
LOG_LEVEL=DEBUG
SERPAPI_API_KEY=sua_chave_da_serpapi
Explicação das variáveis:

REDIS_HOST: Endereço do servidor Redis (padrão: localhost).
REDIS_PORT: Porta do servidor Redis (padrão: 6379).
REDIS_DB: Número do banco de dados Redis (padrão: 0).
LOG_LEVEL: Nível de log desejado (opções: DEBUG, INFO, WARNING, ERROR).
SERPAPI_API_KEY: Sua chave de API do SerpAPI (crie uma conta em SerpAPI).
4. Inicie o Servidor
Para rodar a API localmente, execute o seguinte comando:

python app.py
O servidor estará disponível em: http://localhost:5000.

Endpoints

1. /processar_audio (Método: POST)
Este endpoint recebe um arquivo de áudio, transcreve o conteúdo, realiza uma pesquisa na web e retorna a transcrição, os resultados da pesquisa e uma resposta em áudio.

Requisição

Método: POST
URL: /processar_audio
Headers:
Content-Type: multipart/form-data
Body:
audio (obrigatório): Um arquivo de áudio (nos formatos ogg, mp3 ou wav).
Exemplo de Requisição (usando curl):

curl -X POST http://localhost:5000/processar_audio -F "audio=@seu_arquivo.mp3"
Resposta

A resposta será um JSON com os seguintes campos:

transcricao: O texto transcrito do áudio.
filtrado: O texto filtrado com base em palavras-chave como "pesquisar" ou "buscar".
resultados: Os resultados da pesquisa na web (se a transcrição contiver uma consulta).
audio: A resposta gerada em áudio (codificada em base64).
Exemplo de Resposta
{
  "transcricao": "Eu gostaria de pesquisar sobre inteligência artificial",
  "filtrado": "sobre inteligência artificial",
  "resultados": [
    {
      "titulo": "O que é inteligência artificial?",
      "descricao": "A inteligência artificial é o campo da ciência da computação que desenvolve máquinas...",
      "link": "https://www.exemplo.com/artigo1"
    },
    {
      "titulo": "Inteligência artificial no mercado de trabalho",
      "descricao": "O impacto da inteligência artificial no mercado de trabalho tem sido um tema recorrente...",
      "link": "https://www.exemplo.com/artigo2"
    },
    {
      "titulo": "O futuro da inteligência artificial",
      "descricao": "A inteligência artificial continua a evoluir rapidamente, trazendo novas possibilidades para diversas áreas...",
      "link": "https://www.exemplo.com/artigo3"
    }
  ],
  "audio": "base64encodedAudioData=="
}
Códigos de Erro

A API pode retornar os seguintes erros:

400 - Bad Request: Caso o arquivo de áudio não seja enviado ou seja inválido.
404 - Not Found: Quando nenhum resultado relevante é encontrado na pesquisa.
500 - Internal Server Error: Quando ocorre um erro no servidor.
Exemplo de Erro
{
  "error": "Nenhum áudio enviado."
}
Exemplo de Uso

1. Enviar um arquivo de áudio para transcrição e pesquisa
Você envia um arquivo de áudio (por exemplo, "pesquisar inteligência artificial").
A API transcreve o áudio e filtra o texto para buscar na web.
A API retorna a transcrição, os resultados da pesquisa e uma resposta em áudio.
2. Cache de Resultados
Caso a pesquisa já tenha sido realizada anteriormente, a API retorna os resultados armazenados em cache, economizando tempo e recursos.

Requisitos

Certifique-se de ter as seguintes bibliotecas instaladas:

Flask
requests
python-dotenv
redis
SpeechRecognition
PyDub
gTTS
Contribuições

Contribuições são bem-vindas! Se você encontrar um bug ou tiver uma sugestão de melhoria, fique à vontade para abrir um issue ou enviar um pull request.

Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.

requirements.txt
Flask
requests
python-dotenv
redis
SpeechRecognition
PyDub
gTTS
