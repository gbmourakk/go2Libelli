from datetime import datetime
from extensions import db


class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=True)
    conteudo = db.Column(db.Text, nullable=True)
    perguntas = db.Column(db.Text, nullable=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False)
    conteudo_id = db.Column(db.Integer, db.ForeignKey("conteudos.id"), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    disciplina = db.relationship("Disciplina", back_populates="quizzes")
    conteudo_relacionado = db.relationship("Conteudo", back_populates="quizzes")

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, titulo=None, conteudo=None, perguntas=None):
        if titulo is not None: self.titulo = titulo
        if conteudo is not None: self.conteudo = conteudo
        if perguntas is not None: self.perguntas = perguntas
        db.session.commit()
        return self

    def deletar(self):
        db.session.delete(self); db.session.commit()

    @staticmethod
    def permitidos():
        return {"titulo", "conteudo", "perguntas"}

    @staticmethod
    def listar_todos(): return Quiz.query.order_by(Quiz.id.asc()).all()
    @staticmethod
    def buscar_por_id(id): return db.session.get(Quiz, id)
    @staticmethod
    def listar_por_disciplina(disciplina_id): return Quiz.query.filter_by(disciplina_id=disciplina_id).order_by(Quiz.id.asc()).all()
    @staticmethod
    def listar_por_conteudo(conteudo_id): return Quiz.query.filter_by(conteudo_id=conteudo_id).order_by(Quiz.id.asc()).all()


    def to_dict(self):
        return {"id": self.id, "tipo": "quiz", "titulo": self.titulo, "conteudo": self.conteudo,
                "perguntas": self.perguntas, "disciplina_id": self.disciplina_id,
                "conteudo_id": self.conteudo_id,
                "criado_em": self.criado_em.isoformat() if self.criado_em else None}
