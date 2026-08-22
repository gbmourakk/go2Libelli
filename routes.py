from controllers.comentario_controller import ComentarioController
from controllers.conteudo_controller import ConteudoController
from controllers.disciplina_controller import DisciplinaController
from controllers.motor_ia_controller import MotorIAController
from controllers.quiz_controller import QuizController
from controllers.resumo_controller import ResumoController
from controllers.revisao_controller import RevisaoController
from controllers.usuario_controller import UsuarioController


def register_routes(app):
    app.register_blueprint(
        UsuarioController.blueprint, url_prefix="/api/usuarios"
    )
    app.register_blueprint(
        DisciplinaController.blueprint, url_prefix="/api/disciplinas"
    )
    app.register_blueprint(
        ConteudoController.blueprint, url_prefix="/api/conteudos"
    )
    app.register_blueprint(
        ComentarioController.blueprint, url_prefix="/api/comentarios"
    )
    app.register_blueprint(
        QuizController.blueprint, url_prefix="/api/quizzes"
    )
    app.register_blueprint(
        ResumoController.blueprint, url_prefix="/api/resumos"
    )
    app.register_blueprint(
        RevisaoController.blueprint, url_prefix="/api/revisoes"
    )
    app.register_blueprint(
        MotorIAController.blueprint, url_prefix="/api/motor-ia"
    )
