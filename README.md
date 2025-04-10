# Agent Factory

O objetivo deste projeto é criar um "auto-pilot" para desenvolvimento de software, usando como base a sua própria base de conhecimento. Ele integra conceitos de IA, vetores de conhecimento (para busca e armazenamento de arquivos), além de endpoints que expõem funcionalidade de upload, criação de "knowledge bases", e chats inteligentes.

## Sumário

1. [Arquitetura Geral](#arquitetura-geral)  
2. [Principais Pastas](#principais-pastas)  
3. [Como Instalar](#como-instalar)  
4. [Como Executar](#como-executar)  
5. [Como Usar](#como-usar)  
6. [Considerações Finais](#considerações-finais)

---

## Arquitetura Geral

A arquitetura do projeto se baseia em camadas e serviços que se conectam para viabilizar um assistente de desenvolvimento autônomo:

- **Camada de Endpoint (FastAPI):** Expõe rotas para criação de chats, upload de arquivos .zip, criação e consulta de vetores de conhecimento, etc.  
- **Camada de Negócio (Business):** Implementa a lógica de cada funcionalidade (por exemplo, como lidar com chats, arquivos e vetores).  
- **Camada de Domínio (Domain):** Define modelos de dados (usando Pydantic) que representam entidades fundamentais como Chat, Project, File e Vector.  
- **Camada de Banco de Dados (Database):** Implementa interações com o MongoDB para persistência de dados.  
- **Camada de Ferramentas (Tool):** Fornece funções específicas que podem ser invocadas pela IA (por exemplo, executar um comando do sistema ou um comando curl).  
- **Camada de Agente (Agent):** Integra a lógica de "Agentes" responsáveis por orquestrar ferramentas e lidar com prompts, utilizando bibliotecas externas de IA.

### Fluxo Simplificado

1. Um usuário envia uma requisição para algum endpoint, por exemplo, /v1/files, com um arquivo ZIP.  
2. Esse endpoint chama a regra de negócio (Business) correspondente (FileBusiness), que valida o conteúdo, processa e faz a persistência no banco.  
3. Para rodar funções de IA (como criação de vetores, query, etc.), a aplicação se apoia na biblioteca "OpenAI" e em classes responsáveis por gerenciar esses vetores (VectorBusiness).  
4. Para chats, a aplicação salva conversas, chama a IA (ChatBusiness) e retorna a resposta.  

Com isso, o app se mantém organizado e extensível.

---

## Principais Pastas

A estrutura principal fica em "src/", contendo:

1. **agent/**  
   - Contém a lógica de agentes de IA (por exemplo, "coder.py").

2. **business/**  
   - Lógica de negócio para cada funcionalidade:  
     - chat_business.py  
     - file_business.py  
     - vector_business.py  

3. **domain/**  
   - Modelos de domínio e entidades: Chat, Project, File, Vector, etc.

4. **endpoint/**  
   - Endpoints do FastAPI, divididos por tema: chat_endpoint, file_endpoint, vector_endpoint.

5. **database/**  
   - Classe para conectar e manipular dados no MongoDB (mongo_db_client.py).

6. **model/**  
   - Modelos de request/response exclusivos para transporte de dados na API.

7. **tool/**  
   - Funções utilitárias que podem ser executadas pela IA, como comandos de subprocess.

8. **router/**  
   - Define o roteador principal do FastAPI, agregando todos os endpoints.

---

## Como Instalar

1. **Clonar o repositório**  
   Certifique-se de ter o Git instalado e execute:
   ```
   git clone <URL_do_repositorio.git>
   ```
   Em seguida, entre na pasta do projeto:
   ```
   cd the_architect/back
   ```

2. **Criar um ambiente virtual (opcional mas recomendado)**  
   ```
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # No Windows, use: venv\Scripts\activate
   ```

3. **Instalar as dependências**  
   Geralmente é usado um arquivo requirements.txt ou Pipfile. Se existir um requirements.txt, faça:
   ```
   pip install -r requirements.txt
   ```
   Se houver outro gerenciador de pacotes (Poetry, Pipenv, etc.), siga as instruções correspondentes.

4. **Configurar acesso ao MongoDB**  
   Este projeto espera um MongoDB rodando localmente na porta 27017, com um usuário "admin" e senha "123" (de acordo com o arquivo "app.py"). Ajuste conforme necessário.

---

## Como Executar

1. **Inicie o servidor**  
   Dentro do diretório "back/":
   ```
   python src/app.py
   ```
   - O aplicativo FastAPI será inicializado, por padrão na porta 8080 (conforme definido em app.py).

2. **Acesse a documentação da API (Swagger)**  
   - No navegador, abra:  
     ```
     http://localhost:8080/docs
     ```
   - Você poderá visualizar todas as rotas disponíveis e fazer testes ali mesmo.

---

## Como Usar

1. **Upload de Arquivos**  
   - Faça um POST em "/coder-buddy/v1/files" com um arquivo ZIP, informando o form field "project_name".  
   - O sistema extrairá e enviará os arquivos para a API da OpenAI, gerando um "Project" com vários "Files".

2. **Criar um "Knowledge Base" (Vetores)**  
   - Pelo endpoint "/coder-buddy/v1/vectors", envie um POST com um JSON contendo o nome do seu novo vetor.  
   - O retorno será o ID do vector store criado.

3. **Associar um Project ao Vetor**  
   - Usando "/coder-buddy/v1/vectors/{vector_id}/project", você pode adicionar um projeto existente a um vector store, carregando aqueles arquivos no modelo de vetores.

4. **Chat**  
   - Para criar um chat, faça um POST em "/coder-buddy/v1/chat" com o objeto contendo "name" e a lista de ferramentas (tools).  
   - Para enviar mensagens, use "/coder-buddy/v1/chat/{uuid}/message". Ele irá registrar a conversa e responder usando IA.

---

## Considerações Finais

Esta aplicação é um protótipo para um sistema de desenvolvimento automatizado, usando IA para analisar, interpretar e até gerar código. A arquitetura é modular, permitindo fácil extensão com novas funcionalidades ou integração com outras APIs de IA.

Sinta-se à vontade para contribuir, relatar problemas ou enviar sugestões para melhoria. Bom desenvolvimento! 
