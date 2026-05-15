from flask import Blueprint, request
from models import periodos_model as model
from models import lancamento_model as lancamentos_model
from views import periodos_view as view

periodos_bp = Blueprint("periodos", __name__, url_prefix="/periodos")


@periodos_bp.get("/")
def listar():
    """GET /periodos — lista todos os períodos contábeis."""
    return view.render_lista(model.listar_todos())


@periodos_bp.get("/<int:periodo_id>")
def detalhar(periodo_id: int):
    """GET /periodos/<id> — retorna um período pelo ID."""
    periodo = model.buscar_por_id(periodo_id)
    if periodo is None:
        return view.render_erro("Período não encontrado.", status=404)
    return view.render_periodo(periodo)


@periodos_bp.post("/")
def criar():
    """POST /periodos — abre um novo período contábil."""
    dados = request.get_json(force=True, silent=True) or {}

    descricao = dados.get("descricao", "").strip()
    data_inicio = dados.get("data_inicio", "").strip()
    data_fim = dados.get("data_fim", "").strip()

    if not descricao:
        return view.render_erro("Campo 'descricao' é obrigatório.")
    if not data_inicio:
        return view.render_erro("Campo 'data_inicio' é obrigatório (formato: YYYY-MM-DD).")
    if not data_fim:
        return view.render_erro("Campo 'data_fim' é obrigatório (formato: YYYY-MM-DD).")
    if data_fim < data_inicio:
        return view.render_erro("'data_fim' não pode ser anterior a 'data_inicio'.")

    periodo = model.criar(descricao=descricao, data_inicio=data_inicio, data_fim=data_fim)
    return view.render_periodo(periodo), 201


@periodos_bp.post("/<int:periodo_id>/fechar")
def fechar(periodo_id: int):
    """POST /periodos/<id>/fechar — encerra o período (irreversível)."""
    dados = request.get_json(force=True, silent=True) or {}
    fechado_por = dados.get("fechado_por", "sistema").strip()

    sucesso, mensagem = model.fechar(periodo_id, fechado_por=fechado_por)
    if not sucesso:
        return view.render_erro(mensagem)

    periodo = model.buscar_por_id(periodo_id)
    return view.render_periodo(periodo)


@periodos_bp.get("/<int:periodo_id>/lancamentos")
def lancamentos_do_periodo(periodo_id: int):
    """GET /periodos/<id>/lancamentos — lançamentos do período (filtro por data)."""
    periodo = model.buscar_por_id(periodo_id)
    if periodo is None:
        return view.render_erro("Período não encontrado.", status=404)

    todos = lancamentos_model.listar_todos()
    do_periodo = [
        l.to_dict() for l in todos
        if periodo.data_inicio <= l.data <= periodo.data_fim
    ]
    return view.render_json(do_periodo)


@periodos_bp.get("/<int:periodo_id>/balancete")
def balancete(periodo_id: int):
    """GET /periodos/<id>/balancete — consolidado de movimentações do período."""
    periodo = model.buscar_por_id(periodo_id)
    if periodo is None:
        return view.render_erro("Período não encontrado.", status=404)

    todos = lancamentos_model.listar_todos()
    do_periodo = [l for l in todos if periodo.data_inicio <= l.data <= periodo.data_fim]

    total_debito = sum(l.valor for l in do_periodo if l.tipo == "debito")
    total_credito = sum(l.valor for l in do_periodo if l.tipo == "credito")

    return view.render_json({
        "periodo": periodo.to_dict(),
        "total_debito": total_debito,
        "total_credito": total_credito,
        "saldo": total_credito - total_debito,
        "lancamentos": [l.to_dict() for l in do_periodo],
    })
