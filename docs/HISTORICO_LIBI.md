# Histórico da Libi IA

## Como funciona

1. O aluno escreve no chat. O frontend chama `POST /api/conversas/enviar`.
2. `ConversaController` recebe os dados e usa o ID da sessão (`g.usuario.id`).
3. `EnviarMensagemService` valida a entrada, busca até 12 mensagens anteriores da conversa e chama `MotorIAService`.
4. Se a IA responder, o Service salva a pergunta e a resposta em uma única transação SQLAlchemy. Se a chamada falhar, nada é salvo.
5. A interface recarrega as conversas pelo SQLite, mesmo após atualizar a página.

## Arquivos

- `models/conversa.py` e `models/mensagem.py`: as duas entidades do banco.
- `services/conversa/`: enviar, listar, buscar e excluir conversas.
- `controllers/conversa_controller.py`: rotas HTTP da funcionalidade.
- `frontend/chat.js`: mensagens e navegação entre conversas.
- `frontend/api.js`: chamadas HTTP.

Não foi criado um Repository porque as operações do histórico são CRUD simples nos Models. As consultas especializadas dos outros módulos continuam nos três Repositories existentes.

## Endpoints

| Método | Rota | Finalidade |
| --- | --- | --- |
| `GET` | `/api/conversas/` | Lista somente as conversas do usuário logado |
| `GET` | `/api/conversas/<id>` | Recupera as mensagens, se a conversa pertence ao usuário |
| `POST` | `/api/conversas/enviar` | Recebe `texto`, `modo` e `conversa_id` opcional; responde e salva |
| `DELETE` | `/api/conversas/<id>` | Exclui a conversa e suas mensagens |

## Testes para a banca

- Pergunte sobre um tema, atualize a página e abra o histórico.
- Pergunte "E quais foram as consequências?" e mostre que a resposta usa a pergunta anterior.
- Entre com outro usuário e confirme que o histórico não aparece.
- Demonstre que erros do Gemini não criam conversas vazias.

A rota antiga `/api/motor-ia/gerar` foi mantida para compatibilidade, mas a tela Libi IA usa as novas rotas para persistir o histórico.
