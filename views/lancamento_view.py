from flask import jsonify, Response
from models.lancamento_model import Lancamento
from typing import List


def render_lista(lancamentos: List[Lancamento]) -> Response:
    """Retorna a lista de lançamentos como JSON."""
    return jsonify([l.to_dict() for l in lancamentos])


def render_lancamento(lancamento: Lancamento) -> Response:
    """Retorna um único lançamento como JSON."""
    return jsonify(lancamento.to_dict())


def render_erro(mensagem: str, status: int = 400) -> Response:
    """Retorna uma mensagem de erro padronizada."""
    return jsonify({"erro": mensagem}), status
