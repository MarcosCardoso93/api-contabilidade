from typing import Optional
from models.extensions import db


class Lancamento(db.Model):
    __tablename__ = "lancamentos"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)   # "debito" ou "credito"
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.String(10), nullable=False)   # YYYY-MM-DD
    conta_id = db.Column(db.Integer, db.ForeignKey("contas.id"), nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "valor": self.valor,
            "data": self.data,
            "conta_id": self.conta_id,
        }


def listar_todos():
    return Lancamento.query.all()


def buscar_por_id(lancamento_id: int):
    return db.session.get(Lancamento, lancamento_id)


def criar(descricao: str, tipo: str, valor: float, data: str,
          conta_id: Optional[int] = None) -> "Lancamento":
    lancamento = Lancamento(descricao=descricao, tipo=tipo, valor=valor, data=data, conta_id=conta_id)
    db.session.add(lancamento)
    db.session.commit()
    return lancamento
