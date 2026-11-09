# Libelli

O Libelli é um projeto escolar para ajudar o aluno a organizar as matérias e estudar com mais praticidade. Além de guardar conteúdos e anotações, o sistema usa o Google Gemini para criar resumos, exercícios e planos de estudo.

## Tecnologias

- **Frontend:** HTML, CSS e JavaScript, sem framework.
- **Backend:** Python e Flask, com API HTTP.
- **Banco de dados:** SQLite e SQLAlchemy. Existe também uma configuração opcional para MySQL.
- **Inteligência artificial:** API do Google Gemini.

O frontend roda separado do Flask e se comunica com ele pelo arquivo `frontend/api.js`.

## Como executar

É preciso ter Python instalado. No terminal, dentro da pasta do projeto:

```powershell
cd backend
python -m pip install -r requirements.txt
copy .env.example .env
python app.py
```

Abra o arquivo `backend/.env` e coloque sua chave em `GEMINI_API_KEY`. O modelo é definido por `GEMINI_MODEL`; escolha um modelo disponível para sua chave. As funções sem IA continuam disponíveis mesmo sem essa configuração.

Depois, abra `frontend/login.html` com o Live Server, usando `127.0.0.1`. Por padrão, a API Flask responde em `http://127.0.0.1:5000`. Se usar outra porta, altere o endereço em `frontend/api.js`.

## Funcionalidades implementadas

As 20 operações documentadas na entrega original são:

### Matérias e conteúdos

1. Cadastrar matéria.
2. Listar matérias cadastradas.
3. Editar matéria.
4. Excluir matéria.
5. Cadastrar conteúdo de estudo.
6. Listar conteúdos.
7. Editar conteúdo.
8. Excluir conteúdo.
9. Pesquisar estudos por palavra-chave, matéria e tipo de material.
10. Gerar e salvar resumo de conteúdo com IA.

### Comentários, resumos, quizzes e revisões

11. Cadastrar comentário em um estudo.
12. Listar comentários de uma matéria.
13. Editar comentário.
14. Excluir comentário.
15. Editar resumo.
16. Excluir resumo.
17. Editar quiz.
18. Excluir quiz.
19. Atualizar data e situação de uma revisão.
20. Excluir revisão agendada.

### Outros recursos disponíveis

- Histórico da Libi IA: iniciar uma conversa, reabrir as anteriores ou excluí-las. Ao responder, a Libi recebe as 12 mensagens mais recentes como contexto. Cada usuário acessa somente suas próprias conversas.

- Cadastro de usuário, login e logout.
- Conversa com a **Libi IA**, com histórico salvo no SQLite e contexto das mensagens anteriores.
- Geração de quizzes com Gemini a partir dos materiais de estudo.
- **Plano Inteligente:** o aluno escolhe matéria, assunto, duração, tempo diário e dificuldade; o Gemini gera um cronograma que pode ser salvo, consultado e excluído.
- Agendamento e consulta de revisões.

### Quatro casos principais que não são CRUD

Para a demonstração da banca, os casos de uso mais relevantes são:

1. **Gerar resumo com IA:** transformar um conteúdo cadastrado em um resumo e salvá-lo.
2. **Gerar quiz com IA:** criar questões a partir de um conteúdo e salvar o resultado.
3. **Conversar com a Libi IA com memória:** continuar conversas usando o histórico salvo no SQLite e receber respostas contextualizadas do Gemini.
4. **Gerar plano de estudos:** criar um cronograma personalizado a partir das informações do aluno e salvá-lo no SQLite.


## Organização do projeto

```text
frontend/             Páginas, estilos e JavaScript
backend/
  app.py              Inicialização do Flask
  routes.py           Registro das rotas
  controllers/        Recebem as requisições
  services/           Executam os casos de uso
  models/             Entidades e CRUD com SQLAlchemy
  repositories/       Consultas específicas ao banco
docs/                 Diagramas e material para a banca
```

O caminho de uma operação é, em geral:

**Tela → API Flask → Controller → Service → Model/Repository → SQLite**.

Os Repositories atuais estão ligados a **Usuário**, **Disciplina** e **Conteúdo**. A busca que reúne diferentes materiais fica no `BuscarEstudosService`, pois *Estudo* não é uma tabela do banco.

## Testes

Na pasta `backend`:

```powershell
python -m unittest discover -s tests -v
```

Além dos testes automatizados, vale conferir no navegador: cadastro e login, isolamento entre duas contas, criação e pesquisa de materiais, geração com Gemini, reabertura do histórico da Libi, e persistência dos dados após atualizar a página e reiniciar o Flask. Os testes que simulam respostas da IA não substituem uma chamada real ao Gemini.

## Material da apresentação

- `docs/diagrama_classes.png` e `docs/diagrama_classes.puml`: classes do domínio e relacionamentos.
## Histórico de conversas da Libi

A Libi salva perguntas e respostas nas tabelas `conversas` e `mensagens` do SQLite. O chat mostra as conversas da conta logada. Ao continuar uma conversa, o Service recupera até 12 mensagens anteriores e envia esse contexto ao Gemini. A pergunta e a resposta são salvas juntas **somente após** a IA responder.

A criação das tabelas novas ocorre na inicialização do Flask (`db.create_all()`); as tabelas e os dados anteriores não são substituídos. O botão **Nova** começa uma conversa, que só é registrada no banco quando a primeira resposta é gerada.

Para testar apenas o chat, execute na pasta `backend`:

```powershell
python -m unittest discover -s tests -p "test_conversas.py" -v
```

Faça também o teste manual: envie duas perguntas relacionadas, atualize a página, abra a conversa salva e faça login com outra conta para confirmar que o histórico é privado.
