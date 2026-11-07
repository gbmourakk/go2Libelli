from datetime import datetime
from extensions import db


class Mensagem(db.Model):
    __tablename__ = "mensagens"

    id = db.Column(db.Integer, primary_key=True)
    conversa_id = db.Column(db.Integer, db.ForeignKey("conversas.id"), nullable=False, index=True)
    papel = db.Column(db.String(12), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    conversa = db.relationship("Conversa", back_populates="mensagens")

    @staticmethod
    def listar_recentes(conversa_id, limite=12):
        recentes = (Mensagem.query.filter_by(conversa_id=conversa_id)
                    .order_by(Mensagem.id.desc()).limit(limite).all())
        return list(reversed(recentes))

    def to_dict(self):
        return {
            "id": self.id,
            "papel": self.papel,
            "conteudo": self.conteudo,
            "criado_em": self.criado_em.isoformat(),
        }
