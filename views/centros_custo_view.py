from flask import jsonify, Response
from models.centros_custo_model import CentroCusto
from typing import List


def render_lista(centros: List[CentroCusto]) -> Response:
    return jsonify([c.to_dict() for c in centros])


def render_centro(centro: CentroCusto) -> Response:
    return jsonify(centro.to_dict())


def render_erro(mensagem: str, status: int = 400) -> Response:
    return jsonify({"erro": mensagem}), status


def render_json(dados) -> Response:
    return jsonify(dados)
