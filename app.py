from flask import Flask, render_template
from config import Config
from models.extensions import db
from controllers.lancamento_controller import lancamento_bp
from controllers.contas_controller import contas_bp
from controllers.centros_custo_controller import centros_bp, rateio_bp
from controllers.periodos_controller import periodos_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Registro dos blueprints (controllers)
app.register_blueprint(lancamento_bp)
app.register_blueprint(contas_bp)
app.register_blueprint(centros_bp)
app.register_blueprint(rateio_bp)
app.register_blueprint(periodos_bp)


@app.get("/")
def index():
    return render_template("index.html")


def _seed():
    """Popula o banco com dados iniciais caso esteja vazio."""
    from models.lancamento_model import Lancamento
    from models.contas_model import Conta
    from models.centros_custo_model import CentroCusto
    from models.periodos_model import PeriodoContabil

    if not Lancamento.query.first():
        db.session.add_all([
            Lancamento(descricao="Venda de produtos", tipo="credito", valor=1000.00, data="2026-01-10"),
            Lancamento(descricao="Aluguel da loja", tipo="debito", valor=2000.00, data="2026-01-15"),
        ])

    if not Conta.query.first():
        # Nível 1 — contas raiz
        c_ativo = Conta(codigo="1", descricao="ATIVO", tipo="ativo", natureza="devedora", aceita_lancamento=False)
        c_passivo = Conta(codigo="2", descricao="PASSIVO", tipo="passivo", natureza="credora", aceita_lancamento=False)
        c_receitas = Conta(codigo="3", descricao="RECEITAS", tipo="receita", natureza="credora", aceita_lancamento=False)
        c_despesas = Conta(codigo="4", descricao="DESPESAS", tipo="despesa", natureza="devedora", aceita_lancamento=False)
        db.session.add_all([c_ativo, c_passivo, c_receitas, c_despesas])
        db.session.flush()  # garante IDs antes das filhas

        # Nível 2
        c_ativo_circ = Conta(codigo="1.1", descricao="ATIVO CIRCULANTE", tipo="ativo", natureza="devedora",
                             aceita_lancamento=False, conta_pai_id=c_ativo.id)
        c_rec_serv = Conta(codigo="3.1", descricao="Receita de Serviços", tipo="receita", natureza="credora",
                           aceita_lancamento=True, conta_pai_id=c_receitas.id)
        c_desp_op = Conta(codigo="4.1", descricao="Despesas Operacionais", tipo="despesa", natureza="devedora",
                          aceita_lancamento=True, conta_pai_id=c_despesas.id)
        db.session.add_all([c_ativo_circ, c_rec_serv, c_desp_op])
        db.session.flush()

        # Nível 3
        db.session.add(Conta(codigo="1.1.01", descricao="Caixa", tipo="ativo", natureza="devedora",
                             aceita_lancamento=True, conta_pai_id=c_ativo_circ.id))

    if not CentroCusto.query.first():
        db.session.add_all([
            CentroCusto(codigo="CC-001", descricao="Comercial"),
            CentroCusto(codigo="CC-002", descricao="Tecnologia"),
            CentroCusto(codigo="CC-003", descricao="Administrativo"),
        ])

    if not PeriodoContabil.query.first():
        db.session.add_all([
            PeriodoContabil(descricao="Janeiro/2026", data_inicio="2026-01-01", data_fim="2026-01-31",
                            status="fechado", fechado_em="2026-02-05T10:00:00", fechado_por="admin"),
            PeriodoContabil(descricao="Maio/2026", data_inicio="2026-05-01", data_fim="2026-05-31", status="aberto"),
        ])

    db.session.commit()


with app.app_context():
    db.create_all()
    _seed()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
