from flask import Blueprint, request
from models import centros_custo_model as model
from models import lancamento_model as lancamentos_model
from views import centros_custo_view as view

centros_bp = Blueprint("centros_custo", __name__, url_prefix="/centros-de-custo")


@centros_bp.get("/")
def listar():
    """GET /centros-de-custo — lista todos os centros de custo."""
    return view.render_lista(model.listar_todos())


@centros_bp.get("/<int:centro_id>")
def detalhar(centro_id: int):
    """GET /centros-de-custo/<id> — retorna um centro pelo ID."""
    centro = model.buscar_por_id(centro_id)
    if centro is None:
        return view.render_erro("Centro de custo não encontrado.", status=404)
    return view.render_centro(centro)


@centros_bp.post("/")
def criar():
    """POST /centros-de-custo — cria um novo centro de custo."""
    dados = request.get_json(force=True, silent=True) or {}

    codigo = dados.get("codigo", "").strip()
    descricao = dados.get("descricao", "").strip()

    if not codigo:
        return view.render_erro("Campo 'codigo' é obrigatório.")
    if not descricao:
        return view.render_erro("Campo 'descricao' é obrigatório.")

    centro = model.criar(codigo=codigo, descricao=descricao)
    return view.render_centro(centro), 201


@centros_bp.patch("/<int:centro_id>/desativar")
def desativar(centro_id: int):
    """PATCH /centros-de-custo/<id>/desativar — desativa um centro sem excluí-lo."""
    sucesso, mensagem = model.desativar(centro_id)
    if not sucesso:
        return view.render_erro(mensagem, status=404)
    return view.render_json({"mensagem": mensagem})


@centros_bp.get("/<int:centro_id>/lancamentos")
def lancamentos_do_centro(centro_id: int):
    """GET /centros-de-custo/<id>/lancamentos — lançamentos vinculados ao centro."""
    centro = model.buscar_por_id(centro_id)
    if centro is None:
        return view.render_erro("Centro de custo não encontrado.", status=404)

    ids = model.lancamentos_do_centro(centro_id)
    todos = lancamentos_model.listar_todos()
    resultado = [l.to_dict() for l in todos if l.id in ids]
    return view.render_json(resultado)


# Rota de rateio registrada no blueprint de lançamentos via prefixo /lancamentos
rateio_bp = Blueprint("rateio", __name__, url_prefix="/lancamentos")


@rateio_bp.post("/<int:lancamento_id>/rateio")
def registrar_rateio(lancamento_id: int):
    """POST /lancamentos/<id>/rateio — define o rateio por centro de custo."""
    lancamento = lancamentos_model.buscar_por_id(lancamento_id)
    if lancamento is None:
        return view.render_erro("Lançamento não encontrado.", status=404)

    dados = request.get_json(force=True, silent=True) or {}
    itens = dados.get("rateios", [])

    if not itens:
        return view.render_erro("Campo 'rateios' é obrigatório e não pode estar vazio.")

    sucesso, mensagem = model.registrar_rateio(lancamento_id, itens)
    if not sucesso:
        return view.render_erro(mensagem)

    rateios = model.rateios_do_lancamento(lancamento_id)
    return view.render_json({
        "mensagem": mensagem,
        "rateios": [r.to_dict() for r in rateios],
    }), 201
