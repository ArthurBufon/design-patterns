# ⚡ Cursor Setup — Arthur

## 🔌 MCPs Configurados

> Arquivo: `/home/arthur/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "context7": {
      "command": "/home/arthur/.nvm/versions/node/v24.15.0/bin/npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "filesystem": {
      "command": "/home/arthur/.nvm/versions/node/v24.15.0/bin/npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/arthur/projects"]
    },
    "github": {
      "command": "/home/arthur/.nvm/versions/node/v24.15.0/bin/npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "xxxx"
      }
    }
  }
}
```

### 📦 MCPs Ativos

| MCP | Função |
|---|---|
| 📚 **Context7** | Docs atualizadas das libs em tempo real |
| 📁 **Filesystem** | Agent lê/escreve arquivos do projeto |
| 🐙 **GitHub** | Cria branches, PRs e issues sem sair do Cursor |

### 🔜 MCPs Desejáveis (próximos passos)

| MCP | Função |
|---|---|
| 🎭 **Playwright** | Testes E2E automatizados |
| 🗄️ **MySQL** | Consulta banco direto pelo agent |

> ⚠️ **Regra:** máximo 5 MCPs ativos. Cada um consome tokens de contexto.

---

## 🧩 Plugins Instalados

### ⚡ Superpowers

**O que é:** Metodologia completa de desenvolvimento agentico. Ativa automaticamente skills de brainstorming, planejamento, TDD e debugging antes de qualquer implementação.

**Instalação no Cursor Agent chat:**
```
/add-plugin superpowers
```
> Instalar como **"Add for myself"** (global) — funciona em todos os projetos.

**Como funciona no dia a dia:**

```
Antes:  você pede feature → agent pula direto pro código ❌
Depois: você pede feature → brainstorming → plano → você valida → implementa ✅
```

**Skills automáticas ativadas:**

| Skill | Quando ativa |
|---|---|
| 🧠 **brainstorming** | Ao iniciar qualquer feature nova |
| 📋 **writing-plans** | Após aprovar o design |
| 🧪 **test-driven-development** | Durante implementação |
| 🐛 **systematic-debugging** | Ao encontrar bugs |
| 👀 **requesting-code-review** | Entre tarefas |

> ✅ Nenhum comando manual necessário — tudo é automático.

---

## 🛠️ Stack do Projeto

| Tecnologia | Versão |
|---|---|
| Laravel | latest |
| Inertia.js | latest |
| React + TypeScript | latest |
| Tailwind CSS | latest |
| Docker (Laravel Sail) | latest |
| WSL2 (Ubuntu) | — |
| Node (nvm) | v24.15.0 |
