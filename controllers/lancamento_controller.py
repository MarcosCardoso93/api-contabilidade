import json
from flask import Blueprint, request
from models import lancamento_model as model
from views import lancamento_view as view

lancamento_bp = Blueprint("lancamentos", __name__, url_prefix="/lancamentos")


@lancamento_bp.get("/")
def listar():
    """GET /lancamentos — lista todos os lançamentos."""
    lancamentos = model.listar_todos()
    return view.render_lista(lancamentos)


@lancamento_bp.get("/<int:lancamento_id>")
def detalhar(lancamento_id: int):
    """GET /lancamentos/<id> — retorna um lançamento pelo ID."""
    lancamento = model.buscar_por_id(lancamento_id)
    if lancamento is None:
        return view.render_erro("Lançamento não encontrado.", status=404)
    return view.render_lancamento(lancamento)


@lancamento_bp.post("/")
def criar():
    """POST /lancamentos — cria um novo lançamento."""
    try:
        dados = request.get_json(force=True, silent=True) or json.loads(request.data or b"{}")
    except (json.JSONDecodeError, Exception):
        dados = {}

    descricao = dados.get("descricao", "").strip()
    tipo = dados.get("tipo", "").strip().lower()
    valor = dados.get("valor")
    data = dados.get("data", "").strip()

    # Validações
    if not descricao:
        return view.render_erro("Campo 'descricao' é obrigatório.")

    if tipo not in ["debito", "credito"]:
        return view.render_erro("Campo 'tipo' deve ser 'debito' ou 'credito'.")

    if valor is None:
        return view.render_erro("Campo 'valor' é obrigatório.")

    if not data:
        return view.render_erro("Campo 'data' é obrigatório (formato: YYYY-MM-DD).")

    lancamento = model.criar(descricao=descricao, tipo=tipo, valor=float(valor), data=data)
    return view.render_lancamento(lancamento), 201
