from flask import Blueprint, g, jsonify, request

from services.conversa.buscar_conversa_service import BuscarConversaService
from services.conversa.enviar_mensagem_service import EnviarMensagemService
from services.conversa.excluir_conversa_service import ExcluirConversaService
from services.conversa.listar_conversas_service import ListarConversasService
from services.motor_ia.motor_ia_service import ErroMotorIA


class ConversaController:
    blueprint = Blueprint("conversa_controller", __name__)

    @staticmethod
    def listar():
        conversas = ListarConversasService().execute(g.usuario.id)
        return jsonify([conversa.to_dict() for conversa in conversas])

    @staticmethod
    def buscar(conversa_id):
        conversa = BuscarConversaService().execute(g.usuario.id, conversa_id)
        if not conversa:
            return jsonify({"erro": "Conversa não encontrada."}), 404
        return jsonify({
            **conversa.to_dict(),
            "mensagens": [mensagem.to_dict() for mensagem in conversa.mensagens],
        })

    @staticmethod
    def enviar():
        try:
            conversa, resposta = EnviarMensagemService().execute(
                g.usuario.id, request.get_json(silent=True) or {}
            )
            return jsonify({
                "conversa": conversa.to_dict(),
                "mensagem": resposta.to_dict(),
            }), 201
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except LookupError as erro:
            return jsonify({"erro": str(erro)}), 404
        except ErroMotorIA as erro:
            return jsonify({"erro": str(erro)}), 503

    @staticmethod
    def excluir(conversa_id):
        if not ExcluirConversaService().execute(g.usuario.id, conversa_id):
            return jsonify({"erro": "Conversa não encontrada."}), 404
        return "", 204


ConversaController.blueprint.add_url_rule("/", view_func=ConversaController.listar, methods=["GET"])
ConversaController.blueprint.add_url_rule("/enviar", view_func=ConversaController.enviar, methods=["POST"])
ConversaController.blueprint.add_url_rule("/<int:conversa_id>", view_func=ConversaController.buscar, methods=["GET"])
ConversaController.blueprint.add_url_rule("/<int:conversa_id>", view_func=ConversaController.excluir, methods=["DELETE"])
