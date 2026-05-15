from typing import Optional
from datetime import datetime
from models.extensions import db

STATUS_VALIDOS = {"aberto", "em_fechamento", "fechado"}


class PeriodoContabil(db.Model):
    __tablename__ = "periodos_contabeis"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.String(10), nullable=False)   # YYYY-MM-DD
    data_fim = db.Column(db.String(10), nullable=False)      # YYYY-MM-DD
    status = db.Column(db.String(20), default="aberto")
    fechado_em = db.Column(db.String(30), nullable=True)
    fechado_por = db.Column(db.String(100), nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "descricao": self.descricao,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "status": self.status,
            "fechado_em": self.fechado_em,
            "fechado_por": self.fechado_por,
        }


def listar_todos():
    return PeriodoContabil.query.all()


def buscar_por_id(periodo_id: int) -> Optional[PeriodoContabil]:
    return db.session.get(PeriodoContabil, periodo_id)


def criar(descricao: str, data_inicio: str, data_fim: str) -> PeriodoContabil:
    periodo = PeriodoContabil(descricao=descricao, data_inicio=data_inicio, data_fim=data_fim)
    db.session.add(periodo)
    db.session.commit()
    return periodo


def fechar(periodo_id: int, fechado_por: str = "sistema") -> tuple[bool, str]:
    periodo = buscar_por_id(periodo_id)
    if periodo is None:
        return False, "Período não encontrado."
    if periodo.status == "fechado":
        return False, "Período já está fechado. Esta operação é irreversível."
    periodo.status = "fechado"
    periodo.fechado_em = datetime.now().isoformat()
    periodo.fechado_por = fechado_por
    db.session.commit()
    return True, "Período encerrado com sucesso."


def periodo_esta_aberto(periodo_id: int) -> bool:
    periodo = buscar_por_id(periodo_id)
    return periodo is not None and periodo.status == "aberto"
