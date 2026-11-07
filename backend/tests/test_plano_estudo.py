"""Testes HTTP do Plano Inteligente (Gemini simulado, SQLite temporário).

Execute: cd backend && python -m unittest discover -s tests -p 'test_plano_estudo.py' -v
"""
import os
import tempfile
import unittest
from unittest.mock import patch

_tmp = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_tmp.name, "planos-teste.db")
os.environ["SECRET_KEY"] = "chave-testes-nunca-publicar"

from app import app  # noqa: E402
from extensions import db  # noqa: E402
from models.plano_estudo import PlanoEstudo  # noqa: E402
from services.motor_ia.motor_ia_service import ErroMotorIA  # noqa: E402


class TestePlanoEstudo(unittest.TestCase):
    def setUp(self):
        self.contexto = app.app_context()
        self.contexto.push()
        db.drop_all()
        db.create_all()
        self.cliente = app.test_client()
        self.outro = app.test_client()
        self.cab = {"X-Libelli-Request": "1"}
        self.aluno_id = self.registrar(self.cliente, "aluno-a@teste.com")
        self.outro_id = self.registrar(self.outro, "aluno-b@teste.com")
        self.disciplina_id = self.cliente.post("/api/disciplinas/", json={
            "nome": "Matemática", "usuario_id": self.aluno_id
        }, headers=self.cab).get_json()["id"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.contexto.pop()

    def registrar(self, cliente, email):
        criado = cliente.post("/api/usuarios/", json={
            "nome": "Aluno", "email": email, "senha": "senha-de-teste-123"
        }, headers=self.cab)
        self.assertEqual(criado.status_code, 201)
        self.assertEqual(cliente.post("/api/usuarios/login", json={
            "email": email, "senha": "senha-de-teste-123"
        }, headers=self.cab).status_code, 200)
        return criado.get_json()["id"]

    def pedido(self, disciplina_id=None):
        return {
            "disciplina_id": disciplina_id or self.disciplina_id,
            "tema": "Funções do segundo grau",
            "dias": 7,
            "minutos_por_dia": 60,
            "dificuldade": "iniciante",
        }

    @patch("services.plano_estudo.gerar_plano_estudo_service.MotorIAService.execute",
           return_value="## Dia 1\n- Rever conceitos por 60 minutos\n\n## Dia 2\n- Resolver exercícios")
    def test_gerar_listar_abrir_e_excluir(self, ia):
        resposta = self.cliente.post("/api/planos/gerar", json=self.pedido(), headers=self.cab)
        self.assertEqual(resposta.status_code, 201)
        plano = resposta.get_json()
        self.assertEqual(plano["tema"], "Funções do segundo grau")
        self.assertEqual(plano["dias"], 7)
        self.assertEqual(plano["disciplina_nome"], "Matemática")
        self.assertIn("Dia 1", plano["cronograma"])
        self.assertEqual(ia.call_args.args[0], "plano")
        self.assertIn("60 minutos", ia.call_args.args[1])
        self.assertEqual(PlanoEstudo.query.count(), 1)
        self.assertEqual(self.cliente.get("/api/planos/?usuario_id=" + str(self.aluno_id)).status_code, 200)
        self.assertEqual(len(self.cliente.get("/api/planos/?usuario_id=" + str(self.aluno_id)).get_json()), 1)
        self.assertEqual(self.cliente.get("/api/planos/" + str(plano["id"])).get_json()["id"], plano["id"])
        self.assertEqual(self.cliente.delete("/api/planos/" + str(plano["id"]), headers=self.cab).status_code, 204)
        self.assertEqual(PlanoEstudo.query.count(), 0)

    @patch("services.plano_estudo.gerar_plano_estudo_service.MotorIAService.execute",
           return_value="## Dia 1\nTópicos")
    def test_contas_isoladas(self, ia):
        # Outro aluno não pode gerar plano usando disciplina da primeira conta.
        self.assertEqual(self.outro.post("/api/planos/gerar", json=self.pedido(), headers=self.cab).status_code, 403)
        self.assertEqual(ia.call_count, 0)
        plano_id = self.cliente.post("/api/planos/gerar", json=self.pedido(), headers=self.cab).get_json()["id"]
        self.assertEqual(self.outro.get("/api/planos/" + str(plano_id)).status_code, 403)
        self.assertEqual(self.outro.delete("/api/planos/" + str(plano_id), headers=self.cab).status_code, 403)
        self.assertEqual(self.outro.get("/api/planos/?usuario_id=" + str(self.aluno_id)).status_code, 403)
        self.assertEqual(self.outro.get("/api/planos/?usuario_id=" + str(self.outro_id)).get_json(), [])

    @patch("services.plano_estudo.gerar_plano_estudo_service.MotorIAService.execute")
    def test_validacoes_nao_consultam_ia_nem_salvam(self, ia):
        invalidos = [
            {"tema": "x"}, {"dias": 0}, {"dias": 31}, {"dias": 2.5},
            {"minutos_por_dia": 14}, {"minutos_por_dia": 481},
            {"dificuldade": "super dificil"},
        ]
        for mudanca in invalidos:
            with self.subTest(mudanca=mudanca):
                dados = {**self.pedido(), **mudanca}
                self.assertEqual(self.cliente.post("/api/planos/gerar", json=dados, headers=self.cab).status_code, 400)
        self.assertEqual(PlanoEstudo.query.count(), 0)
        ia.assert_not_called()

    @patch("services.plano_estudo.gerar_plano_estudo_service.MotorIAService.execute",
           side_effect=ErroMotorIA("Gemini indisponível"))
    def test_erro_ia_nao_salva(self, _ia):
        res = self.cliente.post("/api/planos/gerar", json=self.pedido(), headers=self.cab)
        self.assertEqual(res.status_code, 503)
        self.assertEqual(PlanoEstudo.query.count(), 0)

    def test_sem_login(self):
        anonimo = app.test_client()
        self.assertEqual(anonimo.get("/api/planos/?usuario_id=1").status_code, 401)
        self.assertEqual(anonimo.post("/api/planos/gerar", json=self.pedido(), headers=self.cab).status_code, 401)


if __name__ == "__main__":
    unittest.main()
