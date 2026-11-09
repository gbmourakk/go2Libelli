                                                                    
from flask import Blueprint, g, jsonify, request
from services.motor_ia.motor_ia_service import ErroMotorIA
from services.plano_estudo.gerar_plano_estudo_service import GerarPlanoEstudoService
from services.plano_estudo.listar_planos_estudo_service import ListarPlanosEstudoService
from services.plano_estudo.buscar_plano_estudo_service import BuscarPlanoEstudoService
from services.plano_estudo.deletar_plano_estudo_service import DeletarPlanoEstudoService


class PlanoEstudoController:
    blueprint = Blueprint("plano_estudo_controller", __name__)

    @staticmethod
    def gerar():
        try:
            plano = GerarPlanoEstudoService().execute(g.usuario.id, request.get_json(silent=True) or {})
            return jsonify(plano.to_dict()), 201
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except ErroMotorIA as erro:
            return jsonify({"erro": str(erro)}), 503

    @staticmethod
    def listar():
        planos = ListarPlanosEstudoService().execute(g.usuario.id)
        return jsonify([plano.to_dict() for plano in planos])

    @staticmethod
    def buscar(plano_id):
        plano = BuscarPlanoEstudoService().execute(g.usuario.id, plano_id)
        if not plano:
            return jsonify({"erro": "Plano não encontrado."}), 404
        return jsonify(plano.to_dict())

    @staticmethod
    def deletar(plano_id):
        if not DeletarPlanoEstudoService().execute(g.usuario.id, plano_id):
            return jsonify({"erro": "Plano não encontrado."}), 404
        return "", 204


PlanoEstudoController.blueprint.add_url_rule("/", view_func=PlanoEstudoController.listar, methods=["GET"])
PlanoEstudoController.blueprint.add_url_rule("/gerar", view_func=PlanoEstudoController.gerar, methods=["POST"])
PlanoEstudoController.blueprint.add_url_rule("/<int:plano_id>", view_func=PlanoEstudoController.buscar, methods=["GET"])
PlanoEstudoController.blueprint.add_url_rule("/<int:plano_id>", view_func=PlanoEstudoController.deletar, methods=["DELETE"])
