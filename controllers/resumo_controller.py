from flask import Blueprint, jsonify, request

from services.resumo.atualizar_resumo_service import AtualizarResumoService
from services.resumo.buscar_resumo_service import BuscarResumoService
from services.resumo.criar_resumo_service import CriarResumoService
from services.resumo.deletar_resumo_service import DeletarResumoService
from services.resumo.gerar_resumo_service import GerarResumoService
from services.resumo.listar_resumos_service import ListarResumosService


class ResumoController:
    blueprint = Blueprint("resumo_controller", __name__)

    @staticmethod
    def listar():
        resumos = ListarResumosService().execute(
            request.args.get("disciplina_id", type=int)
        )
        return jsonify([resumo.to_dict() for resumo in resumos])

    @staticmethod
    def buscar(resumo_id):
        resumo = BuscarResumoService().execute(resumo_id)
        if not resumo:
            return jsonify({"erro": "Resumo não encontrado."}), 404
        return jsonify(resumo.to_dict())

    @staticmethod
    def criar():
        try:
            resumo = CriarResumoService().execute(request.get_json() or {})
            return jsonify(resumo.to_dict()), 201
        except (ValueError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def atualizar(resumo_id):
        resumo = AtualizarResumoService().execute(resumo_id, request.get_json() or {})
        if not resumo:
            return jsonify({"erro": "Resumo não encontrado."}), 404
        return jsonify(resumo.to_dict())

    @staticmethod
    def deletar(resumo_id):
        if not DeletarResumoService().execute(resumo_id):
            return jsonify({"erro": "Resumo não encontrado."}), 404
        return "", 204

    @staticmethod
    def gerar():
        dados = request.get_json() or {}
        try:
            resumo = GerarResumoService().execute(
                dados["conteudo_id"], dados.get("titulo")
            )
            return jsonify(resumo.to_dict()), 201
        except (ValueError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400


ResumoController.blueprint.add_url_rule("/", view_func=ResumoController.listar, methods=["GET"])
ResumoController.blueprint.add_url_rule("/", view_func=ResumoController.criar, methods=["POST"])
ResumoController.blueprint.add_url_rule("/gerar", view_func=ResumoController.gerar, methods=["POST"])
ResumoController.blueprint.add_url_rule("/<int:resumo_id>", view_func=ResumoController.buscar, methods=["GET"])
ResumoController.blueprint.add_url_rule("/<int:resumo_id>", view_func=ResumoController.atualizar, methods=["PUT"])
ResumoController.blueprint.add_url_rule("/<int:resumo_id>", view_func=ResumoController.deletar, methods=["DELETE"])
