                                                    

                                                                                                     
                                                               
   

import os
import tempfile
import unittest

_tmp = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_tmp.name, "repositorios.db")
os.environ["SECRET_KEY"] = "chave-de-teste-nao-usar-em-producao"

from app import app              
from extensions import db              
from models.usuario import Usuario              
from models.disciplina import Disciplina              
from models.conteudo import Conteudo              
from models.comentario import Comentario              
from models.resumo import Resumo              
from models.quiz import Quiz              
from models.revisao import Revisao              
from repositories.usuario_repository import UsuarioRepository              
from repositories.disciplina_repository import DisciplinaRepository              
from repositories.conteudo_repository import ConteudoRepository              
from services.conteudo.buscar_estudos_service import BuscarEstudosService              


class TestRepositories(unittest.TestCase):
    def setUp(self):
        self.contexto = app.app_context()
        self.contexto.push()
        db.drop_all()
        db.create_all()

        self.aluno = Usuario(nome="Aluno A", email="aluno-a@teste.com", senha_hash="hash").salvar()
        self.outro = Usuario(nome="Aluno B", email="aluno-b@teste.com", senha_hash="hash").salvar()
        self.matematica = Disciplina(nome="Matemática", usuario_id=self.aluno.id).salvar()
        self.historia = Disciplina(nome="História", usuario_id=self.aluno.id).salvar()
        self.outra_disciplina = Disciplina(nome="Privada", usuario_id=self.outro.id).salvar()

        self.conteudo = Conteudo(
            titulo="Equação do segundo grau",
            conteudo="Bhaskara e delta",
            disciplina_id=self.matematica.id,
        ).salvar()
        self.comentario = Comentario(
            titulo="Minha observação",
            texto="Revisar discriminante",
            disciplina_id=self.matematica.id,
        ).salvar()
        self.resumo = Resumo(
            titulo="Resumo de Álgebra", conteudo="Raízes reais",
            disciplina_id=self.matematica.id,
        ).salvar()
        self.quiz = Quiz(
            titulo="Questões da prova", conteudo="Alternativas",
            perguntas="Pergunta 1", disciplina_id=self.matematica.id,
        ).salvar()
        self.revisao = Revisao(
            titulo="Revisar matemática", conteudo="Fórmulas",
            disciplina_id=self.matematica.id,
        ).salvar()
        self.privado = Conteudo(
            titulo="Segredo da outra conta", conteudo="Não pode aparecer",
            disciplina_id=self.outra_disciplina.id,
        ).salvar()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.contexto.pop()

    def test_usuario_repository_busca_sql_e_contagem(self):
        self.assertEqual(UsuarioRepository.buscar_por_email("aluno-a@teste.com").id, self.aluno.id)
        self.assertIsNone(UsuarioRepository.buscar_por_email("ausente@teste.com"))
        linhas = UsuarioRepository.listar_com_disciplinas_count(self.aluno.id)
        self.assertEqual(len(linhas), 1)
        self.assertEqual(linhas[0]["disciplinas_count"], 2)
        self.assertNotIn("senha_hash", linhas[0])

    def test_disciplina_repository_contagem_sql(self):
        linhas = DisciplinaRepository.listar_com_contagem(self.aluno.id)
        por_id = {d["id"]: d for d in linhas}
        self.assertEqual(len(por_id), 2)
        self.assertEqual(por_id[self.matematica.id]["materiais_count"], 5)
        self.assertEqual(por_id[self.historia.id]["materiais_count"], 0)
        self.assertEqual([d.id for d in DisciplinaRepository.listar_por_usuario(self.aluno.id)],
                         [self.matematica.id, self.historia.id])

    def test_conteudo_repository_sql_restringe_usuario(self):
        encontrados = ConteudoRepository.listar_para_busca(self.aluno.id)
        self.assertEqual([conteudo.id for conteudo in encontrados], [self.conteudo.id])
        self.assertEqual(ConteudoRepository.listar_para_busca(self.aluno.id, self.outra_disciplina.id), [])

    def test_busca_global_preserva_tipos_filtros_e_ordenacao(self):
        itens = BuscarEstudosService().execute(self.aluno.id)
        self.assertEqual({item["tipo"] for item in itens},
                         {"conteudo", "comentario", "resumo", "quiz", "revisao"})
        self.assertEqual(len(itens), 5)
        self.assertTrue(all(item["disciplina_nome"] == "Matemática" for item in itens))
        self.assertFalse(any("Segredo" in (item.get("titulo") or "") for item in itens))

        filtrado = BuscarEstudosService().execute(self.aluno.id, termo="BHASKARA", tipo="conteudo")
        self.assertEqual(len(filtrado), 1)
        self.assertEqual(filtrado[0]["id"], self.conteudo.id)
        self.assertEqual(BuscarEstudosService().execute(self.aluno.id, disciplina_id=self.outra_disciplina.id), [])
        self.assertEqual(BuscarEstudosService().execute(self.aluno.id, tipo="inexistente"), [])
        self.assertEqual(BuscarEstudosService().execute(self.aluno.id, tipo=""), itens)
        self.assertEqual([item["titulo"] for item in BuscarEstudosService().execute(
            self.aluno.id, ordenar_por="titulo", direcao="ASC"
        )], sorted(item["titulo"] for item in itens))

    def test_filtros_invalidos(self):
        with self.assertRaises(ValueError):
            BuscarEstudosService().execute(None)
        with self.assertRaises(ValueError):
            BuscarEstudosService().execute(self.aluno.id, ordenar_por="sql injection")
        with self.assertRaises(ValueError):
            BuscarEstudosService().execute(self.aluno.id, direcao="DROP")


if __name__ == "__main__":
    unittest.main()
