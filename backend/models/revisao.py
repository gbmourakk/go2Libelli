from datetime import datetime
from extensions import db


class Revisao(db.Model):
    __tablename__ = "revisoes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=True)
    conteudo = db.Column(db.Text, nullable=True)
    data_revisao = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum("pendente", "concluida", name="status_revisao"), default="pendente")
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False)
    conteudo_id = db.Column(db.Integer, db.ForeignKey("conteudos.id"), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    disciplina = db.relationship("Disciplina", back_populates="revisoes")
    conteudo_relacionado = db.relationship("Conteudo", back_populates="revisoes")

    def salvar(self): db.session.add(self); db.session.commit(); return self
    def atualizar(self, titulo=None, conteudo=None, data_revisao=None, status=None):
        if titulo is not None: self.titulo = titulo
        if conteudo is not None: self.conteudo = conteudo
        if data_revisao is not None: self.data_revisao = data_revisao
        if status is not None: self.status = status
        db.session.commit(); return self
    def deletar(self): db.session.delete(self); db.session.commit()
    @staticmethod
    def permitidos():
        return {"titulo", "conteudo", "data_revisao", "status"}

    @staticmethod
    def listar_todos(): return Revisao.query.order_by(Revisao.id.asc()).all()
    @staticmethod
    def buscar_por_id(id): return db.session.get(Revisao, id)
    @staticmethod
    def listar_por_disciplina(disciplina_id): return Revisao.query.filter_by(disciplina_id=disciplina_id).order_by(Revisao.id.asc()).all()
    @staticmethod
    def listar_por_conteudo(conteudo_id): return Revisao.query.filter_by(conteudo_id=conteudo_id).order_by(Revisao.id.asc()).all()

    def to_dict(self):
        return {"id": self.id, "tipo": "revisao", "titulo": self.titulo, "conteudo": self.conteudo,
                "data_revisao": self.data_revisao.isoformat() if self.data_revisao else None,
                "status": self.status, "disciplina_id": self.disciplina_id,
                "conteudo_id": self.conteudo_id,
                "criado_em": self.criado_em.isoformat() if self.criado_em else None}
