from flask import Blueprint, jsonify, request

from services.quiz.atualizar_quiz_service import AtualizarQuizService
from services.quiz.buscar_quiz_service import BuscarQuizService
from services.quiz.criar_quiz_service import CriarQuizService
from services.quiz.deletar_quiz_service import DeletarQuizService
from services.quiz.gerar_quiz_service import GerarQuizService
from services.quiz.listar_quizzes_service import ListarQuizzesService


class QuizController:
    blueprint = Blueprint("quiz_controller", __name__)

    @staticmethod
    def listar():
        quizzes = ListarQuizzesService().execute(
            request.args.get("disciplina_id", type=int)
        )
        return jsonify([quiz.to_dict() for quiz in quizzes])

    @staticmethod
    def buscar(quiz_id):
        quiz = BuscarQuizService().execute(quiz_id)
        if not quiz:
            return jsonify({"erro": "Quiz não encontrado."}), 404
        return jsonify(quiz.to_dict())

    @staticmethod
    def criar():
        try:
            quiz = CriarQuizService().execute(request.get_json() or {})
            return jsonify(quiz.to_dict()), 201
        except (ValueError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def atualizar(quiz_id):
        quiz = AtualizarQuizService().execute(quiz_id, request.get_json() or {})
        if not quiz:
            return jsonify({"erro": "Quiz não encontrado."}), 404
        return jsonify(quiz.to_dict())

    @staticmethod
    def deletar(quiz_id):
        if not DeletarQuizService().execute(quiz_id):
            return jsonify({"erro": "Quiz não encontrado."}), 404
        return "", 204

    @staticmethod
    def gerar():
        dados = request.get_json() or {}
        try:
            quiz = GerarQuizService().execute(
                dados["conteudo_id"], dados.get("titulo")
            )
            return jsonify(quiz.to_dict()), 201
        except (ValueError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400


QuizController.blueprint.add_url_rule("/", view_func=QuizController.listar, methods=["GET"])
QuizController.blueprint.add_url_rule("/", view_func=QuizController.criar, methods=["POST"])
QuizController.blueprint.add_url_rule("/gerar", view_func=QuizController.gerar, methods=["POST"])
QuizController.blueprint.add_url_rule("/<int:quiz_id>", view_func=QuizController.buscar, methods=["GET"])
QuizController.blueprint.add_url_rule("/<int:quiz_id>", view_func=QuizController.atualizar, methods=["PUT"])
QuizController.blueprint.add_url_rule("/<int:quiz_id>", view_func=QuizController.deletar, methods=["DELETE"])
