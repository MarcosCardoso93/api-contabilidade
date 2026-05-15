# API Contábil

API RESTful para gestão de lançamentos contábeis, plano de contas, centros de custo e períodos contábeis. Desenvolvida em Python com Flask e SQLAlchemy, persistência em SQLite.

---

## Requisitos

- Python 3.10+
- pip

## Instalação

```bash
pip install -r requirements.txt
python app.py
```

A API ficará disponível em `http://localhost:5000`.

O banco de dados (`banco.db`) é criado automaticamente na primeira execução, junto com dados iniciais de exemplo.

---

## Estrutura do Projeto

```
projetoTeste/
├── app.py                        # Ponto de entrada da aplicação
├── config.py                     # Configurações (banco, debug, secret key)
├── models/                       # Camada de dados (SQLAlchemy)
│   ├── lancamento_model.py
│   ├── contas_model.py
│   ├── centros_custo_model.py
│   ├── periodos_model.py
│   └── extensions.py             # Instância compartilhada do db
├── controllers/                  # Rotas e lógica HTTP (Blueprints)
├── views/                        # Serialização das respostas JSON
└── templates/                    # Interface web (index.html)
```

---

## Endpoints

Todas as respostas são em `application/json`.

### Lançamentos — `/lancamentos`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/lancamentos` | Lista todos os lançamentos |
| GET | `/lancamentos/<id>` | Retorna um lançamento pelo ID |
| POST | `/lancamentos` | Cria um novo lançamento |
| POST | `/lancamentos/<id>/rateio` | Define o rateio por centro de custo |

#### POST `/lancamentos`

```json
{
  "descricao": "Venda de produtos",
  "tipo": "credito",
  "valor": 1500.00,
  "data": "2026-05-15"
}
```

| Campo | Tipo | Obrigatório | Valores aceitos |
|-------|------|-------------|-----------------|
| `descricao` | string | Sim | — |
| `tipo` | string | Sim | `debito` ou `credito` |
| `valor` | number | Sim | — |
| `data` | string | Sim | Formato `YYYY-MM-DD` |

#### POST `/lancamentos/<id>/rateio`

```json
{
  "rateios": [
    { "centro_custo_id": 1, "percentual": 60 },
    { "centro_custo_id": 2, "percentual": 40 }
  ]
}
```

A soma dos percentuais deve ser exatamente **100**.

---

### Plano de Contas — `/contas`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/contas` | Lista o plano de contas completo |
| GET | `/contas/<id>` | Retorna uma conta pelo ID |
| POST | `/contas` | Cria uma nova conta |
| DELETE | `/contas/<id>` | Exclui uma conta (bloqueada se tiver filhas) |
| GET | `/contas/<id>/lancamentos` | Lista lançamentos associados à conta |
| GET | `/contas/balancete` | Retorna saldo consolidado por conta |

#### POST `/contas`

```json
{
  "codigo": "4.1.01",
  "descricao": "Despesas com Pessoal",
  "tipo": "despesa",
  "natureza": "devedora",
  "aceita_lancamento": true,
  "conta_pai_id": 5
}
```

| Campo | Tipo | Obrigatório | Valores aceitos |
|-------|------|-------------|-----------------|
| `codigo` | string | Sim | — |
| `descricao` | string | Sim | — |
| `tipo` | string | Sim | `ativo`, `passivo`, `pl`, `receita`, `despesa` |
| `natureza` | string | Sim | `devedora` ou `credora` |
| `aceita_lancamento` | boolean | Não | `true` (padrão) ou `false` |
| `conta_pai_id` | integer | Não | ID de uma conta existente |

---

### Centros de Custo — `/centros-de-custo`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/centros-de-custo` | Lista todos os centros de custo |
| GET | `/centros-de-custo/<id>` | Retorna um centro pelo ID |
| POST | `/centros-de-custo` | Cria um novo centro de custo |
| PATCH | `/centros-de-custo/<id>/desativar` | Desativa o centro (sem excluir) |
| GET | `/centros-de-custo/<id>/lancamentos` | Lista lançamentos vinculados ao centro |

#### POST `/centros-de-custo`

```json
{
  "codigo": "CC-004",
  "descricao": "Marketing"
}
```

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| `codigo` | string | Sim |
| `descricao` | string | Sim |

---

### Períodos Contábeis — `/periodos`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/periodos` | Lista todos os períodos |
| GET | `/periodos/<id>` | Retorna um período pelo ID |
| POST | `/periodos` | Abre um novo período contábil |
| POST | `/periodos/<id>/fechar` | Encerra o período (irreversível) |
| GET | `/periodos/<id>/lancamentos` | Lista lançamentos dentro do período |
| GET | `/periodos/<id>/balancete` | Consolidado de débitos, créditos e saldo |

#### POST `/periodos`

```json
{
  "descricao": "Junho/2026",
  "data_inicio": "2026-06-01",
  "data_fim": "2026-06-30"
}
```

| Campo | Tipo | Obrigatório | Formato |
|-------|------|-------------|---------|
| `descricao` | string | Sim | — |
| `data_inicio` | string | Sim | `YYYY-MM-DD` |
| `data_fim` | string | Sim | `YYYY-MM-DD` |

#### POST `/periodos/<id>/fechar`

```json
{
  "fechado_por": "admin"
}
```

> **Atenção:** o fechamento é irreversível. Um período fechado não pode ser reaberto.

---

## Respostas de Erro

Todos os erros seguem o formato:

```json
{
  "erro": "Descrição do problema."
}
```

| Código | Situação |
|--------|----------|
| 400 | Dados inválidos ou regra de negócio violada |
| 404 | Recurso não encontrado |
| 201 | Criação bem-sucedida |
| 200 | Sucesso |

---

## Interface Web

Acesse `http://localhost:5000` para visualizar todos os endpoints disponíveis com exemplos de chamada em **cURL**, **Python** e **JavaScript**.
