# Especificação: recurso **Carro** (boilerplate Python)

Documento de contexto para humanos e para assistentes de IA ao trabalhar em prompts relacionados a **carros** neste boilerplate Python (espelho do Laravel em `boilerplate-laravel`).

---

## 1. Propósito

O recurso **Carro** exemplifica o padrão do projeto:

- **Queries** (`app.queries.carro.queries.CarroQueries`): acesso a dados e consultas reutilizáveis.
- **Services** (`app.services.carro.service.Service` e `app.services.api.carro.service.Service`): orquestração, transações e formatação antes de persistir.

Os nomes dos métodos seguem o padrão REST dos controllers Laravel: **index**, **show**, **store**, **update**, **destroy**.

---

## 2. Domínio e modelo de dados

### 2.1 Model

- Classe: `app.models.carro.Carro`
- Tabela: `carros`
- Campos persistíveis (espelho de `$fillable`): `marca`, `modelo`, `ano`, `cor`, `placa`, `km`
- Tipos: `ano` e `km` como inteiros no modelo SQLAlchemy

### 2.2 Banco (migration)

Arquivo SQL de referência: `database/migrations/2026_05_08_000000_create_carros.sql` (dialeto próximo ao MySQL; adapte para Postgres/SQLite se necessário).

| Coluna        | Observação                          |
|---------------|-------------------------------------|
| `id`          | Chave primária                      |
| `marca`       | String (até 80 caracteres)          |
| `modelo`      | String (até 120 caracteres)        |
| `ano`         | Ano numérico                        |
| `cor`         | Opcional                            |
| `placa`       | Única no banco                      |
| `km`          | Padrão 0                            |
| `created_at` / `updated_at` | Timestamps                     |

Regras adicionais (validação HTTP, unicidade em formulários, etc.) ficam fora deste núcleo; aqui concentram-se **Queries** + **Services**.

---

## 3. Queries (`app.queries.carro.queries.CarroQueries`)

Responsabilidade: montar `select`, aplicar filtros/ordenação e executar CRUD, retornando sempre um **dict** de resultado.

### 3.1 Formato de retorno

- `sucesso` (`bool`)
- `dados` (`dict`; chaves como `lista`, `model`, `id`, conforme o método)
- `erros` (`list[str]`; em falhas usar `formatar_mensagem_erro` em `app/helpers.py`)

### 3.2 `index(filtros: dict)`

- Sucesso: `dados["lista"]` com `list` de instâncias `Carro`.
- Filtros (valores vazios ou `None` são ignorados):
  - `id`: igualdade
  - `marca`, `modelo`: `LIKE` com `%valor%`
  - `ano`: igualdade
  - `placa`: igualdade
- `ordenacao`: opcional, `{"coluna": str, "ordem": "asc"|"desc"}` — **somente** colunas conhecidas do modelo são aceitas (mitigação a injeção em `ORDER BY`).

### 3.3 `show(filtros: dict)`

- Mesmos filtros que `index`, resultado único em `dados["model"]` (`Carro | None`).

### 3.4 `store(dados: dict)`

- `INSERT` via ORM com campos já preparados pelo service.
- Sucesso: `dados["model"]`, `dados["id"]`.

### 3.5 `update(id: int, dados: dict)`

- Carrega por id (falha → exceção capturada e retorno `sucesso: false`), aplica campos e `flush`.

### 3.6 `destroy(id: str | int)`

- Busca por id, `delete` e `flush`. Sucesso quando a exclusão conclui sem erro.

---

## 4. Service web (`app.services.carro.service.Service`)

- Recebe `CarroQueries` e, opcionalmente, um objeto que implementa `MensagensFlash` (substituto de `session()->flash`).
- **`index` / `show`**: repasse às queries.
- **`store` / `update`**: transação (`Session.begin()`); payload com **`_formatar_database`**: só chaves **presentes** (`in` / `array_key_exists`), permitindo atualização parcial.
- **`_normalizar_placa`**: trim, remove espaços internos, maiúsculas.
- **`destroy(carro: Carro)`**: transação; em sucesso chama `mensagem_sucesso` no flash injetado; em erro chama `mensagem_erro`, `logar_erro` e retorno com `formatar_mensagem_erro`.

---

## 5. Service API (`app.services.api.carro.service.Service`)

- Mesma injeção de `CarroQueries` e o mesmo contrato **index / show / store / update / destroy**.
- Sem mensagens de sessão no `destroy` (API stateless).
- Prefixo distinto em `logar_erro` (“Erro API carro …”), como no Laravel.

O método `store` da API chama o mesmo `_formatar_database` que o `update` (no PHP do repositório havia referência inconsistente a `dadosDatabase`).

---

## 6. Helpers (`app/helpers.py`)

- `formatar_mensagem_erro(exc)`: mensagem, arquivo e linha, alinhado ao PHP.
- `somente_numeros(string)`: remove não dígitos.
- `ambiente_dev()`: `True` se `APP_ENV` contiver `desenvolvimento` (tipo `bool`, refletindo o uso real).

---

## 7. Arquivos de referência

| Caminho |
|---------|
| `app/models/carro.py` |
| `app/queries/carro/queries.py` |
| `app/services/carro/service.py` |
| `app/services/api/carro/service.py` |
| `app/helpers.py` |
| `app/database.py` |
| `database/migrations/2026_05_08_000000_create_carros.sql` |

---

## 8. Extensões comuns (fora do escopo mínimo)

- Framework web (FastAPI, Django, etc.) chamando os services.
- Autorização e escopo por usuário.
- Camada de validação (Pydantic / Marshmallow) alinhada ao schema.
- Testes automatizados sobre `store`/`update` e placa duplicada.

Ao alterar comportamento, **atualize este `specs.md`**.
