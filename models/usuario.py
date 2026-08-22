from datetime import datetime
from extensions import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    disciplinas = db.relationship(
        "Disciplina", back_populates="usuario", cascade="all, delete-orphan"
    )

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, nome=None, email=None, senha_hash=None):
        if nome is not None:
            self.nome = nome
        if email is not None:
            self.email = email
        if senha_hash is not None:
            self.senha_hash = senha_hash
        db.session.commit()
        return self

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def listar_todos():
        return Usuario.query.order_by(Usuario.id.asc()).all()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Usuario, id)

    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
