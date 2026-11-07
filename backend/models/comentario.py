from datetime import datetime
from extensions import db


class Comentario(db.Model):
    __tablename__ = "comentarios"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=True)
    texto = db.Column(db.Text, nullable=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False)
    conteudo_id = db.Column(db.Integer, db.ForeignKey("conteudos.id"), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    disciplina = db.relationship("Disciplina", back_populates="comentarios")
    conteudo = db.relationship("Conteudo", back_populates="comentarios")

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, titulo=None, texto=None, conteudo_id=None):
        if titulo is not None:
            self.titulo = titulo
        if texto is not None:
            self.texto = texto
        if conteudo_id is not None:
            self.conteudo_id = conteudo_id
        db.session.commit()
        return self

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def permitidos():
        return {"titulo", "texto", "conteudo_id"}

    @staticmethod
    def listar_todos():
        return Comentario.query.order_by(Comentario.id.asc()).all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Comentario, id)

    @staticmethod
    def listar_por_disciplina(disciplina_id):
        return Comentario.query.filter_by(disciplina_id=disciplina_id).order_by(Comentario.id.asc()).all()


    def to_dict(self):
        return {
            "id": self.id,
            "tipo": "comentario",
            "titulo": self.titulo,
            "conteudo": self.texto,
            "disciplina_id": self.disciplina_id,
            "conteudo_id": self.conteudo_id,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
