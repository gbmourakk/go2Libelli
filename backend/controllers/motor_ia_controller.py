from services.motor_ia.motor_ia_service import ErroMotorIA
from flask import Blueprint, jsonify, request

from services.motor_ia.gerar_texto_livre_service import GerarTextoLivreService


class MotorIAController:
    blueprint = Blueprint("motor_ia_controller", __name__)

    @staticmethod
    def gerar_texto_livre():
        dados = request.get_json() or {}
        try:
            texto = GerarTextoLivreService().execute(
                dados.get("prompt", ""), dados.get("modo", "resumo")
            )
            return jsonify({"texto": texto})
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except ErroMotorIA as erro:
            return jsonify({"erro": str(erro)}), 503


MotorIAController.blueprint.add_url_rule(
    "/gerar", view_func=MotorIAController.gerar_texto_livre, methods=["POST"]
)
