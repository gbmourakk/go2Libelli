"""Plano de estudos personalizado, vinculado a uma disciplina do aluno."""
from datetime import datetime
from extensions import db


class PlanoEstudo(db.Model):
    __tablename__ = "planos_estudo"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    tema = db.Column(db.String(200), nullable=False)
    dias = db.Column(db.Integer, nullable=False)
    minutos_por_dia = db.Column(db.Integer, nullable=False)
    dificuldade = db.Column(db.String(20), nullable=False)
    cronograma = db.Column(db.Text, nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    disciplina = db.relationship("Disciplina", back_populates="planos_estudo")

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def buscar_por_id(identificador):
        return db.session.get(PlanoEstudo, identificador)

    @staticmethod
    def listar_por_usuario(usuario_id):
        """Consulta ORM: devolve somente planos de disciplinas do usuário."""
        from models.disciplina import Disciplina
        return (
            PlanoEstudo.query.join(Disciplina)
            .filter(Disciplina.usuario_id == usuario_id)
            .order_by(PlanoEstudo.criado_em.desc(), PlanoEstudo.id.desc())
            .all()
        )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "tema": self.tema,
            "dias": self.dias,
            "minutos_por_dia": self.minutos_por_dia,
            "dificuldade": self.dificuldade,
            "cronograma": self.cronograma,
            "disciplina_id": self.disciplina_id,
            "disciplina_nome": self.disciplina.nome if self.disciplina else None,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
