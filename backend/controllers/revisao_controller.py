from datetime import datetime

from flask import Blueprint, jsonify, request

from services.revisao.atualizar_revisao_service import AtualizarRevisaoService
from services.revisao.buscar_revisao_service import BuscarRevisaoService
from services.revisao.criar_revisao_service import CriarRevisaoService
from services.revisao.deletar_revisao_service import DeletarRevisaoService
from services.revisao.gerar_revisao_service import GerarRevisaoService
from services.revisao.listar_revisoes_service import ListarRevisoesService


class RevisaoController:
    blueprint = Blueprint("revisao_controller", __name__)

    @staticmethod
    def listar():
        revisoes = ListarRevisoesService().execute(
            request.args.get("disciplina_id", type=int)
        )
        return jsonify([revisao.to_dict() for revisao in revisoes])

    @staticmethod
    def buscar(revisao_id):
        revisao = BuscarRevisaoService().execute(revisao_id)
        if not revisao:
            return jsonify({"erro": "Revisão não encontrada."}), 404
        return jsonify(revisao.to_dict())

    @staticmethod
    def criar():
        dados = request.get_json() or {}
        try:
            if dados.get("data_revisao"):
                dados["data_revisao"] = datetime.fromisoformat(dados["data_revisao"])
            revisao = CriarRevisaoService().execute(dados)
            return jsonify(revisao.to_dict()), 201
        except (ValueError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def atualizar(revisao_id):
        dados = request.get_json() or {}
        try:
            if dados.get("data_revisao"):
                dados["data_revisao"] = datetime.fromisoformat(dados["data_revisao"])
            revisao = AtualizarRevisaoService().execute(revisao_id, dados)
            if not revisao:
                return jsonify({"erro": "Revisão não encontrada."}), 404
            return jsonify(revisao.to_dict())
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def deletar(revisao_id):
        if not DeletarRevisaoService().execute(revisao_id):
            return jsonify({"erro": "Revisão não encontrada."}), 404
        return "", 204

    @staticmethod
    def gerar():
        dados = request.get_json() or {}
        try:
            revisao = GerarRevisaoService().execute(
                dados["conteudo_id"],
                datetime.fromisoformat(dados["data_revisao"]),
            )
            return jsonify(revisao.to_dict()), 201
        except (ValueError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400


RevisaoController.blueprint.add_url_rule("/", view_func=RevisaoController.listar, methods=["GET"])
RevisaoController.blueprint.add_url_rule("/", view_func=RevisaoController.criar, methods=["POST"])
RevisaoController.blueprint.add_url_rule("/gerar", view_func=RevisaoController.gerar, methods=["POST"])
RevisaoController.blueprint.add_url_rule("/<int:revisao_id>", view_func=RevisaoController.buscar, methods=["GET"])
RevisaoController.blueprint.add_url_rule("/<int:revisao_id>", view_func=RevisaoController.atualizar, methods=["PUT"])
RevisaoController.blueprint.add_url_rule("/<int:revisao_id>", view_func=RevisaoController.deletar, methods=["DELETE"])
