# Libelli

Projeto escolar para organizar matérias e conteúdos e ajudar nos estudos com inteligência artificial.

## Tecnologias

- **Frontend:** HTML, CSS e JavaScript.
- **Backend:** Python e Flask (API).
- **Banco:** SQLite com SQLAlchemy.
- **IA:** Google Gemini.

## Funcionalidades

- Cadastro, login e gerenciamento de matérias e conteúdos.
- Comentários, resumos, quizzes e revisões.
- Pesquisa de materiais de estudo.
- Resumos e quizzes gerados com IA.
- Planos de estudo personalizados com IA.
- Chat Libi IA com histórico salvo no SQLite.

## Como executar

No terminal, entre na pasta `backend`:

```powershell
cd backend
python -m pip install -r requirements.txt
copy .env.example .env
python app.py
```

No arquivo `backend/.env`, configure `GEMINI_API_KEY` e, se necessário, `GEMINI_MODEL`. Sem a chave, as funções que usam IA não funcionam.

Abra `frontend/login.html` com o Live Server usando `127.0.0.1`. A API roda em `http://127.0.0.1:5000`.

## Organização

- `frontend/`: páginas, estilos e JavaScript.
- `backend/controllers/`: recebem as requisições.
- `backend/services/`: executam os casos de uso.
- `backend/models/`: entidades e CRUD básico.
- `backend/repositories/`: consultas específicas ao banco.
- `docs/`: diagrama de classes.

**Fluxo:** Frontend → Controller → Service → Model/Repository → SQLite.

## Testes

Na pasta `backend`:

```powershell
python -m unittest discover -s tests -v
```
