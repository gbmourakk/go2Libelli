from datetime import datetime
from extensions import db


class Disciplina(db.Model):
    __tablename__ = "disciplinas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship("Usuario", back_populates="disciplinas")
    conteudos = db.relationship("Conteudo", back_populates="disciplina", cascade="all, delete-orphan")
    comentarios = db.relationship("Comentario", back_populates="disciplina", cascade="all, delete-orphan")
    quizzes = db.relationship("Quiz", back_populates="disciplina", cascade="all, delete-orphan")
    resumos = db.relationship("Resumo", back_populates="disciplina", cascade="all, delete-orphan")
    revisoes = db.relationship("Revisao", back_populates="disciplina", cascade="all, delete-orphan")

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, nome=None, descricao=None):
        if nome is not None:
            self.nome = nome
        if descricao is not None:
            self.descricao = descricao
        db.session.commit()
        return self

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def listar_todos():
        return Disciplina.query.order_by(Disciplina.id.asc()).all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Disciplina, id)

    @staticmethod
    def listar_por_usuario(usuario_id):
        return Disciplina.query.filter_by(usuario_id=usuario_id).order_by(Disciplina.id.asc()).all()

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "usuario_id": self.usuario_id,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
