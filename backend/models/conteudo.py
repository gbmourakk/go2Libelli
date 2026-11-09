from datetime import datetime
from extensions import db


class Conteudo(db.Model):
    __tablename__ = "conteudos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=True)
    conteudo = db.Column(db.Text, nullable=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    disciplina = db.relationship("Disciplina", back_populates="conteudos")
    comentarios = db.relationship("Comentario", back_populates="conteudo", cascade="all, delete-orphan")
    quizzes = db.relationship("Quiz", back_populates="conteudo_relacionado", cascade="all, delete-orphan")
    resumos = db.relationship("Resumo", back_populates="conteudo_relacionado", cascade="all, delete-orphan")
    revisoes = db.relationship("Revisao", back_populates="conteudo_relacionado", cascade="all, delete-orphan")

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, titulo=None, conteudo=None):
        if titulo is not None:
            self.titulo = titulo
        if conteudo is not None:
            self.conteudo = conteudo
        db.session.commit()
        return self

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def permitidos():
        return {"titulo", "conteudo"}

    @staticmethod
    def listar_todos():
        return Conteudo.query.order_by(Conteudo.id.asc()).all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Conteudo, id)

    @staticmethod
    def listar_por_disciplina(disciplina_id):
        return Conteudo.query.filter_by(disciplina_id=disciplina_id).order_by(Conteudo.id.asc()).all()


    def to_dict(self):
        return {
            "id": self.id,
            "tipo": "conteudo",
            "titulo": self.titulo,
            "conteudo": self.conteudo,
            "disciplina_id": self.disciplina_id,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
