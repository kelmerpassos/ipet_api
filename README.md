# iPET (API)

Este arquivo contem instruções de instalação, estrutura de pastas e os padrões de commit a serem utilizados.

## :book: Padrões de Commit utilizados no projeto

Utilize o commit semântico definido pelas regras abaixo para descrever as intenções de cada commit de seu código:

- ```feat```- indica que seu trecho de código está incluindo um novo recurso ao projeto;
- ```fix``` - indica que seu trecho de código commitado está solucionando um problema (bug fix);
- ```refact``` refere-se a mudanças de refatorações do código que não alteram funcionalidades do projeto mas trazem algum tipo de melhoria na performance do código devido a um code review, por exemplo;
- ```style``` - indica que houve alterações referentes a formatações de código, semicolons, trailing spaces, lint, etc e não inclui alterações em código;
- ```test``` - são utilizados quando há alterações em testes, seja criando, alterando ou excluindo testes unitários. (Não inclui alterações em código);
- ```docs```- indica que houve mudanças na documentação, como por exemplo no Readme do repositório;
- ```build```- utilizados quando houver modificações em arquivos de build e dependências;
- ```ci```- indica mudanças relacionadas a integração contínua (continuous integration).

**_Exemplo de um Commit:_**
```feat: Criação de rotas de produto```
## :file_folder: Organização das pastas
As pastas deste projeto devem ser organizadas conforme exemplo a seguir.

Exemplo árvore base de pastas e arquivos :
```
├── ipet
|   ├── common
│   ├── ext
│       ├── packege1
│          |── models.py
│          |── resources.py
│          |── routes.py
│          |── schemas.py
│       ├── packege2
│          |── models.py
│          |── resources.py
│          |── routes.py
│          |── schemas.py
|   ├── static
│   ├── __init__.py
├── tests
├── docker-compose.yaml
├── Dockerfile
├── settings.toml
├── requirements.txt
├── requirements-dev.txt
├── wsgi.py
```
## :file_folder: Pacotes:
- ```auth```- Pacote de autenticação;
- ```cli```- Pacote de comandos do terminal;
- ```config```- Pacote de configurações;
- ```customer```- Pacote gerenciador do domínio de cliente;
- ```db```- Pacote de gestão das bases de dados;
- ```doc```- Pacote e configuração do OpenAPI;
- ```libs```- Pacote de inicialização de bibliotecas auxiliares;
- ```product```- Pacote gerenciador da domínio de produto.
## :gear: Principais tecnologias:
- [Python 10.5.*](https://www.python.org/)
- [Flask 2.1.*](https://flask.palletsprojects.com/en/2.1.x/)
- [PostgreSQL 14.4](https://www.postgresql.org/about/news/postgresql-144-released-2470/#:~:text=The%20PostgreSQL%20Global%20Development%20Group,data%20corruption%20in%20your%20indexes.)
- [Redis 7.0.*](https://redis.io/docs/getting-started/)
## :book: Variáveis de ambiente
##### **Como criar uma variável de ambiente Linux**
```
$ export VAR="value"
```
##### **Como criar uma variável de ambiente Windows**
```
$ set VAR="value"
```
- ```export ou set```- Comando usado para criar uma variável;
- ```VAR```- Nome da variável;
- ```value```- Próprio valor da variável.

Variáveis de ambiente existentes no sistema.

- ```FLASK_ENV``` - Em qual ambiente o aplicativo flask está sendo executado (Default ```Production```);
- ```FLASK_SECRET_KEY``` - Uma chave secreta que será usada para assinar com segurança o cookie de sessão e pode ser usada para quaisquer outras necessidades relacionadas à segurança por extensões ou seu aplicativo (Default ```chavedesenvolvimento```);
- ```FLASK_SQLALCHEMY_DATABASE_URI``` - O URI do banco de dados que deve ser usado para a conexão (Default ```postgresql+psycopg2://postgres:postgres@db:5432/DBIPet```); 
- ```FLASK_REDIS_URL``` - A URL do redis que deve ser usado para a conexão (Default ```redis://redis:6379/0```);
- ```FLASK_JWT_ACCESS_TOKEN_EXPIRES``` - Por quanto tempo (em segundos) um token de acesso deve ser válido antes de expirar (Default ```3600```);
- ```FLASK_JWT_REFRESH_TOKEN_EXPIRES``` - Por quanto tempo (em segundos) um token de atualização deve ser válido antes de expirar (Default ```604800```);
- ```FLASK_SSH_HOST``` - Host de acesso ao servidor SSH;
- ```FLASK_SSH_PORT``` - Porta de acesso ao servidor SSH (Default ```22```);
- ```FLASK_SSH_USER``` - Usuário de acesso ao servidor SSH;
- ```FLASK_SSH_PASSWORD``` - Senha de acesso ao servidor SSH;
- ```FLASK_DB_FILE_PATH``` - Caminho da base offline de dados, no servidor SSH.
## :traffic_light: Instalação (desenvolvimento) sem docker
##### **Clone o repositório com git clone**
```
$ git clone https://github.com/kelmerpassos/ipet_api.git
```
##### **Acesse a pasta _ipet_**
```
$ cd ipet
```
##### **Crie e ative o ambiente virtual**
```
$ python -m venv venv
```
##### **Em sistemas Linux ou macOS**
```
$ source venv/bin/activate 
```
##### **Em sistema Windows**
```
$ source venv/Scripts/Activate 
```
##### **Instale todas as dependências com o comando pip**
```
$ pip install -r requirements.txt
```
##### **Instale todas as dependências de desenvolvimento com o comando pip**
```
$ pip install -r requirements-dev.txt
```
Faça o download e instalação do PostgreSQL e do Redis:
- [PostgreSQL](https://www.postgresql.org/about/news/postgresql-144-released-2470/#:~:text=The%20PostgreSQL%20Global%20Development%20Group,data%20corruption%20in%20your%20indexes.)
- [Redis](https://redis.io/docs/getting-started/)

Faça a configuração das variáveis de ambiente básicas obrigatórias, vista na seção anterior.

##### **Rode a aplicação**
```
$ flask run
```
:bulb: No VsCode instale as extensões **Python**, **Pylance** para ajudar na identificação de erros de padrão de escrita do código.
