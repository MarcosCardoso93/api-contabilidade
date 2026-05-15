from models.extensions import db


class Lancamento(db.Model):
    __tablename__ = "lancamentos"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)   # "debito" ou "credito"
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.String(10), nullable=False)   # YYYY-MM-DD

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "valor": self.valor,
            "data": self.data,
        }


def listar_todos():
    return Lancamento.query.all()


def buscar_por_id(lancamento_id: int):
    return db.session.get(Lancamento, lancamento_id)


def criar(descricao: str, tipo: str, valor: float, data: str) -> Lancamento:
    lancamento = Lancamento(descricao=descricao, tipo=tipo, valor=valor, data=data)
    db.session.add(lancamento)
    db.session.commit()
    return lancamento
