from datetime import datetime
from extensions import db


class Conversa(db.Model):
    __tablename__ = "conversas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False, index=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    usuario = db.relationship("Usuario", back_populates="conversas")
    mensagens = db.relationship(
        "Mensagem", back_populates="conversa", cascade="all, delete-orphan",
        order_by="Mensagem.id"
    )

    @staticmethod
    def listar_por_usuario(usuario_id):
        return (Conversa.query.filter_by(usuario_id=usuario_id)
                .order_by(Conversa.atualizado_em.desc(), Conversa.id.desc()).all())

    @staticmethod
    def buscar_do_usuario(conversa_id, usuario_id):
        return Conversa.query.filter_by(id=conversa_id, usuario_id=usuario_id).first()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat(),
        }
