from flask import jsonify, Response
from models.contas_model import Conta
from typing import List


def render_lista(contas: List[Conta]) -> Response:
    return jsonify([c.to_dict() for c in contas])


def render_conta(conta: Conta) -> Response:
    return jsonify(conta.to_dict())


def render_erro(mensagem: str, status: int = 400) -> Response:
    return jsonify({"erro": mensagem}), status


def render_balancete(balancete: list) -> Response:
    return jsonify(balancete)
