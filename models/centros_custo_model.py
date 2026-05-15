from typing import Optional, List
from models.extensions import db


class CentroCusto(db.Model):
    __tablename__ = "centros_custo"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    rateios = db.relationship("RateioLancamento", backref="centro", lazy=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "codigo": self.codigo,
            "descricao": self.descricao,
            "ativo": self.ativo,
        }


class RateioLancamento(db.Model):
    __tablename__ = "rateios_lancamento"

    id = db.Column(db.Integer, primary_key=True)
    lancamento_id = db.Column(db.Integer, db.ForeignKey("lancamentos.id"), nullable=False)
    centro_custo_id = db.Column(db.Integer, db.ForeignKey("centros_custo.id"), nullable=False)
    percentual = db.Column(db.Float, nullable=False)

    def to_dict(self) -> dict:
        return {
            "lancamento_id": self.lancamento_id,
            "centro_custo_id": self.centro_custo_id,
            "percentual": self.percentual,
        }


def listar_todos() -> List[CentroCusto]:
    return CentroCusto.query.all()


def buscar_por_id(centro_id: int) -> Optional[CentroCusto]:
    if not centro_id:
        return None
    return db.session.get(CentroCusto, centro_id)


def criar(codigo: str, descricao: str, ativo: bool = True) -> CentroCusto:
    centro = CentroCusto(codigo=codigo, descricao=descricao, ativo=ativo)
    db.session.add(centro)
    db.session.commit()
    return centro


def desativar(centro_id: int) -> tuple[bool, str]:
    centro = buscar_por_id(centro_id)
    if centro is None:
        return False, "Centro de custo não encontrado."
    centro.ativo = False
    db.session.commit()
    return True, "Centro de custo desativado."


def registrar_rateio(lancamento_id: int, itens: list) -> tuple[bool, str]:
    total = sum(i.get("percentual", 0) for i in itens)
    if round(total, 2) != 100.0:
        return False, f"A soma dos percentuais deve ser 100%. Soma atual: {total}%."

    for item in itens:
        if buscar_por_id(item.get("centro_custo_id")) is None:
            return False, f"Centro de custo {item.get('centro_custo_id')} não encontrado."

    RateioLancamento.query.filter_by(lancamento_id=lancamento_id).delete()
    for item in itens:
        db.session.add(RateioLancamento(
            lancamento_id=lancamento_id,
            centro_custo_id=item["centro_custo_id"],
            percentual=item["percentual"],
        ))
    db.session.commit()
    return True, "Rateio registrado com sucesso."


def rateios_do_lancamento(lancamento_id: int) -> List[RateioLancamento]:
    return RateioLancamento.query.filter_by(lancamento_id=lancamento_id).all()


def lancamentos_do_centro(centro_id: int) -> List[int]:
    return [r.lancamento_id for r in RateioLancamento.query.filter_by(centro_custo_id=centro_id).all()]
