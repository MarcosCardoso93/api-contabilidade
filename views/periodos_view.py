from flask import jsonify, Response
from models.periodos_model import PeriodoContabil
from typing import List


def render_lista(periodos: List[PeriodoContabil]) -> Response:
    return jsonify([p.to_dict() for p in periodos])


def render_periodo(periodo: PeriodoContabil) -> Response:
    return jsonify(periodo.to_dict())


def render_erro(mensagem: str, status: int = 400) -> Response:
    return jsonify({"erro": mensagem}), status


def render_json(dados) -> Response:
    return jsonify(dados)
