"""Execute: cd backend && python -m pytest -q tests/test_login.py"""
import os
import tempfile
import unittest

# Banco de teste isolado: não acessa o libelli.db real nem a API Gemini.
_tmp = tempfile.TemporaryDirectory()
os.environ['DATABASE_URL'] = 'sqlite:///' + os.path.join(_tmp.name, 'auth-test.db')
os.environ['SECRET_KEY'] = 'chave-testes-locais-nao-utilizar-em-producao'

from app import app  # noqa: E402
from extensions import db  # noqa: E402


class TesteLogin(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
        self.cliente = app.test_client()
        self.cab = {'X-Libelli-Request': '1'}

    def cadastrar(self, cliente, email):
        return cliente.post('/api/usuarios/', json={
            'nome': 'Estudante', 'email': email, 'senha': 'senha-segura-123'
        }, headers=self.cab)

    def login(self, cliente, email):
        return cliente.post('/api/usuarios/login', json={
            'email': email, 'senha': 'senha-segura-123'
        }, headers=self.cab)

    def test_fluxo_de_cadastro_login_logout(self):
        self.assertEqual(self.cliente.get('/api/usuarios/me').status_code, 401)
        r = self.cadastrar(self.cliente, 'aluno@example.com')
        self.assertEqual(r.status_code, 201)
        self.assertNotIn('senha_hash', r.get_json())
        self.assertEqual(self.cliente.post('/api/usuarios/login', json={
            'email': 'aluno@example.com', 'senha': 'errada'
        }, headers=self.cab).status_code, 401)
        self.assertEqual(self.login(self.cliente, 'aluno@example.com').status_code, 200)
        self.assertEqual(self.cliente.get('/api/usuarios/me').status_code, 200)
        self.assertEqual(self.cliente.post('/api/usuarios/logout', headers=self.cab).status_code, 200)
        self.assertEqual(self.cliente.get('/api/usuarios/me').status_code, 401)

    def test_dados_sao_isolados_entre_usuarios(self):
        outro = app.test_client()
        a = self.cadastrar(self.cliente, 'aluno1@example.com').get_json()
        b = self.cadastrar(outro, 'aluno2@example.com').get_json()
        self.login(self.cliente, 'aluno1@example.com')
        self.login(outro, 'aluno2@example.com')
        r = self.cliente.post('/api/disciplinas/', json={
            'nome': 'Matemática', 'usuario_id': a['id']
        }, headers=self.cab)
        self.assertEqual(r.status_code, 201)
        disc = r.get_json()
        self.assertEqual(outro.get('/api/disciplinas/%s' % disc['id']).status_code, 403)
        self.assertEqual(outro.get('/api/disciplinas/?usuario_id=%s' % a['id']).status_code, 403)
        self.assertEqual(outro.get('/api/conteudos/?disciplina_id=%s' % disc['id']).status_code, 403)
        self.assertEqual(outro.post('/api/conteudos/', json={
            'titulo': 'Ataque', 'disciplina_id': disc['id'], 'conteudo': 'texto'
        }, headers=self.cab).status_code, 403)
        self.assertEqual(outro.post('/api/disciplinas/', json={
            'nome': 'Acesso indevido', 'usuario_id': a['id']
        }, headers=self.cab).status_code, 403)
        self.assertEqual(outro.get('/api/disciplinas/com-contagem').status_code, 400)
        self.assertEqual(outro.get('/api/usuarios/').status_code, 403)
        self.assertEqual(outro.get('/api/disciplinas/?usuario_id=%s' % b['id']).status_code, 200)

    def test_mutacao_exige_cabecalho_customizado(self):
        self.cadastrar(self.cliente, 'aluno3@example.com')
        self.login(self.cliente, 'aluno3@example.com')
        r = self.cliente.post('/api/disciplinas/', json={'nome': 'História', 'usuario_id': 1})
        self.assertEqual(r.status_code, 403)


if __name__ == '__main__':
    unittest.main()
