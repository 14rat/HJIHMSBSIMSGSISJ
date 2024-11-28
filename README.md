# API de Processamento de Áudio e Pesquisa na Web

Esta API permite que você envie arquivos de áudio, obtenha transcrições de texto, realize pesquisas na web baseadas em palavras-chave transcritas e receba respostas em áudio com base nos resultados encontrados. Ela utiliza Flask, Redis para cache, SerpAPI para busca na web e Google Text-to-Speech (gTTS) para gerar áudio.

## Funcionalidades

- **Transcrição de Áudio**: Converte áudio em texto utilizando reconhecimento de fala.
- **Pesquisa na Web**: Realiza pesquisas na web com base no conteúdo transcrito do áudio.
- **Resposta em Áudio**: Gera uma resposta em áudio contendo o número de resultados encontrados para a pesquisa.
- **Cache de Resultados**: Utiliza Redis para armazenar os resultados das consultas e evitar requisições repetidas à web.

## Tecnologias Utilizadas

- **Flask**: Framework web para Python.
- **Redis**: Banco de dados em memória utilizado para cache.
- **SpeechRecognition**: Biblioteca para reconhecimento de fala.
- **PyDub**: Biblioteca para manipulação de áudio.
- **gTTS**: API do Google Text-to-Speech para conversão de texto em fala.
- **SerpAPI**: API para realizar buscas na web utilizando o Google.

---

## Pré-Requisitos

- **Python 3.x** (certifique-se de ter o Python 3 instalado no seu ambiente).
- **Redis** (instalado e em execução localmente ou em um servidor remoto).

---

## Instalação

### 1. Clone o Repositório

Clone o repositório para o seu ambiente local:

```bash
git clone https:https://github.com/14rat/HJIHMSBSIMSGSISJ.git
cd API


## Como Usar:

1. **Clone o Repositório**: Baixe o repositório para o seu ambiente local.
2. **Instale as Dependências**: Use `pip install -r requirements.txt` para instalar as bibliotecas necessárias.
3. **Configure as Variáveis de Ambiente**: Adicione suas credenciais de Redis e SerpAPI no arquivo `.env`.
4. **Inicie o Servidor**: Execute `python app.py` para rodar a API localmente.
5. **Faça Requisições**: Use o endpoint `/processar_audio` para enviar arquivos de áudio, processá-los e obter resultados.



