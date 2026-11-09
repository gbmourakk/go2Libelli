                                                                               
import os
import tempfile
import unittest
from unittest.mock import patch

_tmp = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_tmp.name, "chat-test.db")
os.environ["SECRET_KEY"] = "chave-de-teste-local"

from app import app              
from extensions import db              
from models.usuario import Usuario              
from models.conversa import Conversa              
from models.mensagem import Mensagem              
from services.motor_ia.motor_ia_service import ErroMotorIA              


class TestConversa(unittest.TestCase):
    def setUp(self):
        self.contexto = app.app_context()
        self.contexto.push()
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.aluno = Usuario(nome="Aluno A", email="a@chat.test", senha_hash="hash").salvar()
        self.outro = Usuario(nome="Aluno B", email="b@chat.test", senha_hash="hash").salvar()
        self.cliente = app.test_client()
        self.segundo_cliente = app.test_client()
        self.cab = {"X-Libelli-Request": "1"}
        with self.cliente.session_transaction() as sessao:
            sessao["usuario_id"] = self.aluno.id
        with self.segundo_cliente.session_transaction() as sessao:
            sessao["usuario_id"] = self.outro.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.contexto.pop()

    def enviar(self, texto="O que foi a Revolução Francesa?", conversa_id=None, modo="explicar", cliente=None):
        return (cliente or self.cliente).post("/api/conversas/enviar", json={
            "texto": texto, "modo": modo, "conversa_id": conversa_id
        }, headers=self.cab)

    def test_gerar_salvar_reabrir_e_contexto(self):
        with patch("services.conversa.enviar_mensagem_service.MotorIAService.execute", return_value="Foi em 1789.") as gerar:
            resposta = self.enviar()
        self.assertEqual(resposta.status_code, 201)
        conversa_id = resposta.get_json()["conversa"]["id"]
        self.assertIn("Revolução", resposta.get_json()["conversa"]["titulo"])
        self.assertEqual(len(self.cliente.get("/api/conversas/").get_json()), 1)
        self.assertIn("Revolução Francesa", gerar.call_args.args[1])

        with patch("services.conversa.enviar_mensagem_service.MotorIAService.execute", return_value="A queda da monarquia.") as gerar:
            segunda = self.enviar("E quais foram suas consequências?", conversa_id)
        self.assertEqual(segunda.status_code, 201)
        self.assertIn("Foi em 1789", gerar.call_args.args[1])
        self.assertIn("Revolução Francesa", gerar.call_args.args[1])
        self.assertIn("consequências", gerar.call_args.args[1])

        dados = self.cliente.get(f"/api/conversas/{conversa_id}").get_json()
        self.assertEqual([m["papel"] for m in dados["mensagens"]],
                         ["user", "assistant", "user", "assistant"])
        self.assertEqual(dados["mensagens"][-1]["conteudo"], "A queda da monarquia.")

                                                                   
        self.assertEqual(self.cliente.get(f"/api/conversas/{conversa_id}").status_code, 200)
        self.assertEqual(Mensagem.query.filter_by(conversa_id=conversa_id).count(), 4)

    def test_bloqueio_entre_usuarios(self):
        with patch("services.conversa.enviar_mensagem_service.MotorIAService.execute", return_value="Resposta"):
            criado = self.enviar()
        conversa_id = criado.get_json()["conversa"]["id"]
        self.assertEqual(self.segundo_cliente.get("/api/conversas/").get_json(), [])
        self.assertEqual(self.segundo_cliente.get(f"/api/conversas/{conversa_id}").status_code, 404)
        self.assertEqual(self.segundo_cliente.delete(f"/api/conversas/{conversa_id}", headers=self.cab).status_code, 404)
        self.assertEqual(self.enviar("Outra pergunta", conversa_id, cliente=self.segundo_cliente).status_code, 404)
        self.assertEqual(self.cliente.get(f"/api/conversas/{conversa_id}").status_code, 200)

    def test_falha_do_gemini_nao_salva_perguntas_soltas(self):
        with patch("services.conversa.enviar_mensagem_service.MotorIAService.execute", side_effect=ErroMotorIA("Indisponível")):
            resposta = self.enviar()
        self.assertEqual(resposta.status_code, 503)
        self.assertEqual(Conversa.query.count(), 0)
        self.assertEqual(Mensagem.query.count(), 0)

    def test_validacao_e_autenticacao(self):
        self.assertEqual(self.enviar(" ").status_code, 400)
        self.assertEqual(self.enviar("a" * 4001).status_code, 400)
        self.assertEqual(self.enviar(modo="errado").status_code, 400)
        self.assertEqual(self.enviar(conversa_id="abc").status_code, 400)
        self.assertEqual(self.enviar(conversa_id=999).status_code, 404)
        self.assertEqual(app.test_client().get("/api/conversas/").status_code, 401)
        self.assertEqual(self.cliente.post("/api/conversas/enviar", json={"texto": "abc"}).status_code, 403)

    def test_excluir_apaga_mensagens(self):
        with patch("services.conversa.enviar_mensagem_service.MotorIAService.execute", return_value="Resposta"):
            conversa_id = self.enviar().get_json()["conversa"]["id"]
        self.assertEqual(self.cliente.delete(f"/api/conversas/{conversa_id}", headers=self.cab).status_code, 204)
        self.assertIsNone(Conversa.query.filter_by(id=conversa_id).first())
        self.assertEqual(Mensagem.query.filter_by(conversa_id=conversa_id).count(), 0)
        self.assertEqual(self.cliente.get("/api/conversas/").get_json(), [])


if __name__ == "__main__":
    unittest.main()
