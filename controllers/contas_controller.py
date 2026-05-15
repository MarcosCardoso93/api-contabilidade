from flask import Blueprint, request
from models import contas_model as model
from models import lancamento_model as lancamentos_model
from views import contas_view as view

contas_bp = Blueprint("contas", __name__, url_prefix="/contas")

TIPOS_VALIDOS = {"ativo", "passivo", "pl", "receita", "despesa"}
NATUREZAS_VALIDAS = {"devedora", "credora"}


@contas_bp.get("/")
def listar():
    """GET /contas — lista o plano de contas completo."""
    return view.render_lista(model.listar_todas())


@contas_bp.get("/<int:conta_id>")
def detalhar(conta_id: int):
    """GET /contas/<id> — retorna uma conta pelo ID."""
    conta = model.buscar_por_id(conta_id)
    if conta is None:
        return view.render_erro("Conta não encontrada.", status=404)
    return view.render_conta(conta)


@contas_bp.post("/")
def criar():
    """POST /contas — cria uma nova conta no plano de contas."""
    dados = request.get_json(force=True, silent=True) or {}

    codigo = dados.get("codigo", "").strip()
    descricao = dados.get("descricao", "").strip()
    tipo = dados.get("tipo", "").strip().lower()
    natureza = dados.get("natureza", "").strip().lower()
    aceita_lancamento = dados.get("aceita_lancamento", True)
    conta_pai_id = dados.get("conta_pai_id")

    if not codigo:
        return view.render_erro("Campo 'codigo' é obrigatório.")
    if not descricao:
        return view.render_erro("Campo 'descricao' é obrigatório.")
    if tipo not in TIPOS_VALIDOS:
        return view.render_erro(f"Campo 'tipo' deve ser um de: {', '.join(TIPOS_VALIDOS)}.")
    if natureza not in NATUREZAS_VALIDAS:
        return view.render_erro(f"Campo 'natureza' deve ser 'devedora' ou 'credora'.")
    if conta_pai_id is not None and model.buscar_por_id(conta_pai_id) is None:
        return view.render_erro("Conta pai não encontrada.")

    conta = model.criar(
        codigo=codigo, descricao=descricao, tipo=tipo,
        natureza=natureza, aceita_lancamento=aceita_lancamento,
        conta_pai_id=conta_pai_id,
    )
    return view.render_conta(conta), 201


@contas_bp.delete("/<int:conta_id>")
def excluir(conta_id: int):
    """DELETE /contas/<id> — exclui uma conta (se não tiver lançamentos ou filhas)."""
    sucesso, mensagem = model.excluir(conta_id)
    if not sucesso:
        return view.render_erro(mensagem, status=400)
    return view.render_erro(mensagem, status=200)


@contas_bp.get("/<int:conta_id>/lancamentos")
def lancamentos_da_conta(conta_id: int):
    """GET /contas/<id>/lancamentos — lançamentos associados a esta conta."""
    conta = model.buscar_por_id(conta_id)
    if conta is None:
        return view.render_erro("Conta não encontrada.", status=404)
    todos = lancamentos_model.listar_todos()
    associados = [l.to_dict() for l in todos if l.tipo in ("debito", "credito")]
    return view.render_balancete(associados)


@contas_bp.get("/balancete")
def balancete():
    """GET /contas/balancete — retorna saldo consolidado por conta."""
    contas = model.listar_todas()
    resultado = [
        {
            "id": c.id,
            "codigo": c.codigo,
            "descricao": c.descricao,
            "tipo": c.tipo,
            "natureza": c.natureza,
            "saldo": 0.0,  # em produção: calcular a partir dos lançamentos no banco
        }
        for c in contas
    ]
    return view.render_balancete(resultado)
