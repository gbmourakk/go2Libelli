from flask import Blueprint, jsonify, request

from services.disciplina.atualizar_disciplina_service import AtualizarDisciplinaService
from services.disciplina.buscar_disciplina_service import BuscarDisciplinaService
from services.disciplina.criar_disciplina_service import CriarDisciplinaService
from services.disciplina.deletar_disciplina_service import DeletarDisciplinaService
from services.disciplina.listar_disciplinas_com_contagem_service import ListarDisciplinasComContagemService
from services.disciplina.listar_disciplinas_service import ListarDisciplinasService


class DisciplinaController:
    blueprint = Blueprint("disciplina_controller", __name__)

    @staticmethod
    def listar():
        disciplinas = ListarDisciplinasService().execute(
            request.args.get("usuario_id", type=int)
        )
        return jsonify([disciplina.to_dict() for disciplina in disciplinas])

    @staticmethod
    def buscar(disciplina_id):
        disciplina = BuscarDisciplinaService().execute(disciplina_id)
        if not disciplina:
            return jsonify({"erro": "Disciplina não encontrada."}), 404
        return jsonify(disciplina.to_dict())

    @staticmethod
    def criar():
        try:
            disciplina = CriarDisciplinaService().execute(request.get_json() or {})
            return jsonify(disciplina.to_dict()), 201
        except (ValueError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def atualizar(disciplina_id):
        try:
            disciplina = AtualizarDisciplinaService().execute(
                disciplina_id, request.get_json() or {}
            )
            if not disciplina:
                return jsonify({"erro": "Disciplina não encontrada."}), 404
            return jsonify(disciplina.to_dict())
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def deletar(disciplina_id):
        if not DeletarDisciplinaService().execute(disciplina_id):
            return jsonify({"erro": "Disciplina não encontrada."}), 404
        return "", 204

    @staticmethod
    def listar_com_contagem():
        dados = ListarDisciplinasComContagemService().execute(
            request.args.get("usuario_id", type=int)
        )
        return jsonify(dados)


DisciplinaController.blueprint.add_url_rule("/", view_func=DisciplinaController.listar, methods=["GET"])
DisciplinaController.blueprint.add_url_rule("/", view_func=DisciplinaController.criar, methods=["POST"])
DisciplinaController.blueprint.add_url_rule("/<int:disciplina_id>", view_func=DisciplinaController.buscar, methods=["GET"])
DisciplinaController.blueprint.add_url_rule("/<int:disciplina_id>", view_func=DisciplinaController.atualizar, methods=["PUT"])
DisciplinaController.blueprint.add_url_rule("/<int:disciplina_id>", view_func=DisciplinaController.deletar, methods=["DELETE"])
DisciplinaController.blueprint.add_url_rule("/com-contagem", view_func=DisciplinaController.listar_com_contagem, methods=["GET"])
