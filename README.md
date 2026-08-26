# LIBELLI

O Libelli é uma aplicação para organizar disciplinas e conteúdos de estudo. O sistema permite cadastrar matérias, guardar conteúdos e usar o Motor IA para gerar materiais de apoio.

## Arquitetura

```text
Frontend
   ↓
API Flask
   ↓
Controller
   ↓
Service
   ↓
Model / Repository
   ↓
Banco de dados
```

```text
backend/
├── controllers/
├── models/
├── repositories/
├── services/
│   ├── usuario/
│   ├── disciplina/
│   ├── conteudo/
│   ├── comentario/
│   ├── quiz/
│   ├── resumo/
│   ├── revisao/
│   └── motor_ia/
└── database/

frontend/
```

Cada entidade do domínio possui sua própria Model. Não existe herança de uma classe `Anotacao`.

As Controllers são classes e recebem as requisições HTTP. Cada caso de uso possui seu próprio Service, com o método `execute()`. Operações CRUD simples ficam nas Models. Repositories são usados para consultas especiais, como contagens e a busca de estudos com filtros.

## Funcionalidades Implementadas

1. Cadastrar disciplina
2. Listar disciplinas
3. Atualizar disciplina
4. Excluir disciplina
5. Cadastrar conteúdo de estudo
6. Listar conteúdos de estudo
7. Atualizar conteúdo de estudo
8. Excluir conteúdo de estudo
9. Buscar estudos com filtros
10. Gerar e salvar resumo de conteúdo

Além das 10 funcionalidades entregues para a etapa, o sistema também possui geração de quiz e agendamento de revisões pelo frontend e pela API.

## Execução

No terminal:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Por padrão, o projeto usa SQLite e cria `libelli.db` automaticamente.

Para usar MySQL, configure as variáveis no `.env`:

```env
USE_MYSQL=true
DB_USER=root
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=libelli
```

Também é possível informar `DATABASE_URL`.

## Frontend

Com o backend rodando, abra:

```text
frontend/index.html
```

O frontend utiliza a API Flask em:

```text
http://localhost:5000/api
```

## Motor IA

As funcionalidades de geração são encapsuladas em Services específicos (`GerarResumoService`, `GerarQuizService`, `GerarRevisaoService` e `GerarTextoLivreService`). O projeto atual utiliza um gerador de texto de demonstração para permitir a execução sem depender de uma chave externa.

Caso uma API externa de IA seja adicionada, a comunicação deve permanecer encapsulada no Service de integração e as credenciais devem ser fornecidas por variáveis de ambiente.

## Banco de dados

O arquivo `backend/database/create_database.sql` contém a estrutura para MySQL e as Stored Procedures utilizadas pelos Repositories.

O Repository é responsável por encapsular os `CALL` das Stored Procedures. Controllers e Services não executam SQL diretamente.
