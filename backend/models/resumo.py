from datetime import datetime
from extensions import db


class Resumo(db.Model):
    __tablename__ = "resumos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=True)
    conteudo = db.Column(db.Text, nullable=True)
    gerado_por_ia = db.Column(db.Boolean, default=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False)
    conteudo_id = db.Column(db.Integer, db.ForeignKey("conteudos.id"), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    disciplina = db.relationship("Disciplina", back_populates="resumos")
    conteudo_relacionado = db.relationship("Conteudo", back_populates="resumos")

    def salvar(self): db.session.add(self); db.session.commit(); return self
    def atualizar(self, titulo=None, conteudo=None, gerado_por_ia=None):
        if titulo is not None: self.titulo = titulo
        if conteudo is not None: self.conteudo = conteudo
        if gerado_por_ia is not None: self.gerado_por_ia = gerado_por_ia
        db.session.commit(); return self
    def deletar(self): db.session.delete(self); db.session.commit()
    @staticmethod
    def permitidos():
        return {"titulo", "conteudo", "gerado_por_ia"}

    @staticmethod
    def listar_todos(): return Resumo.query.order_by(Resumo.id.asc()).all()
    @staticmethod
    def buscar_por_id(id): return db.session.get(Resumo, id)
    @staticmethod
    def listar_por_disciplina(disciplina_id): return Resumo.query.filter_by(disciplina_id=disciplina_id).order_by(Resumo.id.asc()).all()
    @staticmethod
    def listar_por_conteudo(conteudo_id): return Resumo.query.filter_by(conteudo_id=conteudo_id).order_by(Resumo.id.asc()).all()

    def to_dict(self):
        return {"id": self.id, "tipo": "resumo", "titulo": self.titulo, "conteudo": self.conteudo,
                "gerado_por_ia": bool(self.gerado_por_ia), "disciplina_id": self.disciplina_id,
                "conteudo_id": self.conteudo_id,
                "criado_em": self.criado_em.isoformat() if self.criado_em else None}
