from typing import Optional
from models.extensions import db

TIPOS_VALIDOS = {"ativo", "passivo", "pl", "receita", "despesa"}
NATUREZAS_VALIDAS = {"devedora", "credora"}


class Conta(db.Model):
    __tablename__ = "contas"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)       # ativo|passivo|pl|receita|despesa
    natureza = db.Column(db.String(20), nullable=False)   # devedora|credora
    aceita_lancamento = db.Column(db.Boolean, default=True)
    conta_pai_id = db.Column(db.Integer, db.ForeignKey("contas.id"), nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "codigo": self.codigo,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "natureza": self.natureza,
            "aceita_lancamento": self.aceita_lancamento,
            "conta_pai_id": self.conta_pai_id,
        }


def listar_todas():
    return Conta.query.all()


def buscar_por_id(conta_id: int) -> Optional[Conta]:
    return db.session.get(Conta, conta_id)


def criar(codigo: str, descricao: str, tipo: str, natureza: str,
          aceita_lancamento: bool = True, conta_pai_id: Optional[int] = None) -> Conta:
    conta = Conta(
        codigo=codigo, descricao=descricao, tipo=tipo,
        natureza=natureza, aceita_lancamento=aceita_lancamento,
        conta_pai_id=conta_pai_id,
    )
    db.session.add(conta)
    db.session.commit()
    return conta


def excluir(conta_id: int) -> tuple[bool, str]:
    conta = buscar_por_id(conta_id)
    if conta is None:
        return False, "Conta não encontrada."
    tem_filhas = Conta.query.filter_by(conta_pai_id=conta_id).first() is not None
    if tem_filhas:
        return False, "Conta possui contas filhas — não pode ser excluída."
    db.session.delete(conta)
    db.session.commit()
    return True, "Conta excluída com sucesso."


def registrar_lancamento_na_conta(conta_id: int):
    """Placeholder — com SQLAlchemy o vínculo é gerenciado via FK no lançamento."""
    pass
