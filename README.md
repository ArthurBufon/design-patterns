# 📚 Design Patterns

Um repositório com **padrões de projeto**, exemplos práticas e estruturas recomendadas para desenvolvimento.

---

## 📁 Conteúdo

### 🏗️ `/laravel`
Exemplo de estrutura **padronizada e típica** para um workflow seguindo **SRP (Single Responsibility Principle)**.

### ⚙️ `/cursor`
Exemplos de **rules** (regras) para configuração e padrões de comportamento.

Útil como referência para implementar regras em seus próprios projetos.

---

## 🎯 Para quê serve?

Este repositório é uma **coleção de referências** para:
- ✅ Entender padrões de projeto na prática
- ✅ Consultar estruturas recomendadas
- ✅ Seguir boas práticas de arquitetura
- ✅ Manter código mais organizado e escalável
- ✅ Gerar boilerplate seguindo padrões estruturados e validados

---

## 🤖 Por que isso é importante?

Com o **avanço da IA**, ficou mais importante que nunca:

- **📋 Documentar processos** — IA trabalha melhor com contexto claro
- **🏛️ Padronizar estruturas** — facilita prompts e geração de código consistente
- **🎯 Usar SDD (Specification-Driven Development)** — defina regras e padrões antes de codificar

Uma base bem documentada e padronizada permite que **você e a IA trabalhem juntos de forma mais eficiente e previsível**.

---

## 📚 Conceitos Principais

### 🔍 **Queries**

Arquivos padronizados para **buscas simples, básicas e reutilizáveis** entre serviços do projeto.

Evolução do **Repository Pattern** com implementação mais prática:
- 📁 Crie um diretório `/queries`
- 📄 Um arquivo para cada recurso do projeto
- 💡 Exemplo: `/queries/carro/queries.py`

**Vantagem:** Consultas reutilizáveis e fáceis de manter.

---

### ⚙️ **Services**

Arquivos que lidam com **lógica de negócio específica** para recursos.

Exemplo: para um recurso "carro", o service implementa métodos como:
- `criar_carro()` — lógica de criação
- `validar_carro()` — regras de validação
- `processar_pagamento()` — operações complexas
- etc.

**Vantagem:** Separação clara entre dados (queries) e lógica (services).

---

## 🎬 Padrão REST: Index/Show/Store/Update/Destroy

Nomenclatura padronizada dos **Resource Controllers do Laravel**, mantida entre projetos de **diferentes linguagens**.

| Método | Operação | Descrição |
|--------|----------|-----------|
| **INDEX** | GET `/recurso` | Lista todos os recursos |
| **SHOW** | GET `/recurso/{id}` | Exibe um recurso individual |
| **STORE** | POST `/recurso` | Cria um novo recurso |
| **UPDATE** | PUT `/recurso/{id}` | Atualiza um recurso existente |
| **DESTROY** | DELETE `/recurso/{id}` | Deleta um recurso |

**Vantagem:** Padrão universal, fácil de manter e transferir entre projetos.

---

## 🚀 Como usar?

Explore as pastas, estude os exemplos e adapte para seus projetos!