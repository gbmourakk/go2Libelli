from flask import Blueprint, jsonify, request

from services.conteudo.atualizar_conteudo_service import AtualizarConteudoService
from services.conteudo.buscar_conteudo_service import BuscarConteudoService
from services.conteudo.buscar_estudos_service import BuscarEstudosService
from services.conteudo.criar_conteudo_service import CriarConteudoService
from services.conteudo.deletar_conteudo_service import DeletarConteudoService
from services.conteudo.listar_conteudos_service import ListarConteudosService


class ConteudoController:
    blueprint = Blueprint("conteudo_controller", __name__)

    @staticmethod
    def listar():
        conteudos = ListarConteudosService().execute(
            request.args.get("disciplina_id", type=int)
        )
        return jsonify([conteudo.to_dict() for conteudo in conteudos])

    @staticmethod
    def buscar(conteudo_id):
        conteudo = BuscarConteudoService().execute(conteudo_id)
        if not conteudo:
            return jsonify({"erro": "Conteúdo não encontrado."}), 404
        return jsonify(conteudo.to_dict())

    @staticmethod
    def criar():
        try:
            conteudo = CriarConteudoService().execute(request.get_json() or {})
            return jsonify(conteudo.to_dict()), 201
        except (ValueError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def atualizar(conteudo_id):
        try:
            conteudo = AtualizarConteudoService().execute(
                conteudo_id, request.get_json() or {}
            )
            if not conteudo:
                return jsonify({"erro": "Conteúdo não encontrado."}), 404
            return jsonify(conteudo.to_dict())
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def deletar(conteudo_id):
        if not DeletarConteudoService().execute(conteudo_id):
            return jsonify({"erro": "Conteúdo não encontrado."}), 404
        return "", 204

    @staticmethod
    def buscar_estudos():
        try:
            estudos = BuscarEstudosService().execute(
                usuario_id=request.args.get("usuario_id", type=int),
                termo=request.args.get("termo"),
                disciplina_id=request.args.get("disciplina_id", type=int),
                tipo=request.args.get("tipo"),
                ordenar_por=request.args.get("ordenar_por", "criado_em"),
                direcao=request.args.get("direcao", "desc"),
            )
            return jsonify(estudos)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400


ConteudoController.blueprint.add_url_rule("/", view_func=ConteudoController.listar, methods=["GET"])
ConteudoController.blueprint.add_url_rule("/", view_func=ConteudoController.criar, methods=["POST"])
ConteudoController.blueprint.add_url_rule("/buscar-estudos", view_func=ConteudoController.buscar_estudos, methods=["GET"])
ConteudoController.blueprint.add_url_rule("/<int:conteudo_id>", view_func=ConteudoController.buscar, methods=["GET"])
ConteudoController.blueprint.add_url_rule("/<int:conteudo_id>", view_func=ConteudoController.atualizar, methods=["PUT"])
ConteudoController.blueprint.add_url_rule("/<int:conteudo_id>", view_func=ConteudoController.deletar, methods=["DELETE"])
