#!/usr/bin/env bash
# Cria labels, milestones e as issues do backlog do TaskFlow CLI no GitHub.
#
# Pré-requisitos: GitHub CLI (https://cli.github.com) autenticado com `gh auth login`.
# Uso:            ./scripts/criar-backlog.sh [dono/repositorio]
#
# IMPORTANTE: execute em um repositório SEM issues/PRs prévios, para que a
# numeração (#1 a #19) coincida com as referências usadas nos commits.

set -euo pipefail

REPO="${1:-JulianaPelozo/especificacao-gestao-SDLC}"

echo ">> Criando labels em $REPO"
label() { gh label create "$1" --repo "$REPO" --color "$2" --description "$3" --force; }
label "documentation" "0075ca" "Documentação e especificação"
label "feature"       "a2eeef" "Nova funcionalidade"
label "enhancement"   "84b6eb" "Melhoria de algo existente"
label "bug"           "d73a4a" "Algo não funciona como esperado"
label "refactor"      "fbca04" "Melhoria interna sem mudar comportamento"
label "setup"         "c5def5" "Configuração de ambiente, build e CI"
label "test"          "0e8a16" "Testes automatizados"

echo ">> Criando milestones"
milestone() {
  gh api "repos/$REPO/milestones" -f title="$1" -f description="$2" >/dev/null 2>&1 \
    || echo "   (milestone '$1' já existe)"
}
milestone "v0.1.0" "Documentação de planejamento e setup do projeto"
milestone "v0.2.0" "Núcleo: modelo, persistência, cadastro e listagem"
milestone "v0.3.0" "Gestão completa: editar, concluir/reabrir e remover"
milestone "v0.3.1" "Correção: robustez da persistência"
milestone "v1.0.0" "Busca, ordenação, resumo e documentação final"
milestone "v1.1.0" "Evoluções planejadas"

issue() {
  # $1 título | $2 labels | $3 milestone | stdin corpo
  local body
  body="$(cat)"
  gh issue create --repo "$REPO" --title "$1" --label "$2" --milestone "$3" --body "$body"
}

echo ">> Criando issues (a ordem define a numeração)"

issue "docs: elaborar Termo de Abertura do Projeto (project charter)" "documentation" "v0.1.0" <<'EOF'
Produzir `docs/project-charter.md`.

**Critérios de aceite**
- Dado o documento publicado, quando lido, então contém justificativa e visão geral do produto.
- Contém objetivos SMART numerados.
- Contém escopo preliminar com itens **dentro** e **fora** do escopo.
- Lista stakeholders e público-alvo.
EOF

issue "docs: especificar requisitos funcionais e não funcionais" "documentation" "v0.1.0" <<'EOF'
Produzir `docs/requisitos.md`.

**Critérios de aceite**
- RFs numerados no formato `[RF01]` e rastreáveis para histórias/casos de uso.
- RNFs numerados (`[RNF01]`) cobrindo desempenho, persistência, usabilidade, segurança, portabilidade e manutenibilidade.
- Matriz de rastreabilidade RF → UC → US → Issue.
EOF

issue "docs: especificar casos de uso" "documentation" "v0.1.0" <<'EOF'
Produzir `docs/casos-de-uso.md`.

**Critérios de aceite**
- Descreve os atores envolvidos.
- Cada caso de uso central tem pré-condições, fluxo principal, fluxos alternativos e de exceção e pós-condições.
- Cada caso de uso referencia os RFs que atende.
EOF

issue "docs: escrever histórias de usuário com critérios de aceite" "documentation" "v0.1.0" <<'EOF'
Produzir `docs/user-stories.md`.

**Critérios de aceite**
- Histórias no padrão "Como [ator], quero [ação] para que [valor]".
- Cada história tem critérios de aceite em Gherkin (Dado/Quando/Então).
- Cada história referencia RF e prioridade (MoSCoW).
EOF

issue "docs: criar diagramas de classes, arquitetura (C4) e wireframes da CLI" "documentation" "v0.1.0" <<'EOF'
Produzir `docs/diagramas.md` com diagramas em Mermaid.

**Critérios de aceite**
- Diagrama de classes do domínio e serviços.
- Diagramas C4 de contexto e de contêiner/componentes.
- Rascunho (wireframe textual) das principais saídas da CLI.
EOF

issue "chore: configurar estrutura do projeto, .gitignore e CI" "setup" "v0.1.0" <<'EOF'
**Critérios de aceite**
- Dado o repositório clonado, quando executo `python -m taskflow --version`, então a versão é exibida.
- `.gitignore` ignora `__pycache__`, ambientes virtuais e o arquivo de dados local.
- `pyproject.toml` expõe o comando `taskflow`.
- GitHub Actions executa a suíte de testes em push/PR para `main` e `develop`.
EOF

issue "feat: implementar modelo de domínio Tarefa com validações" "feature" "v0.2.0" <<'EOF'
Relacionado: RF01, RNF05.

**Critérios de aceite**
- Dado um título vazio ou só com espaços, quando crio uma tarefa, então recebo erro de validação.
- Dado uma prioridade fora de `baixa|media|alta`, então recebo erro de validação.
- Dado um prazo fora do formato `AAAA-MM-DD`, então recebo erro de validação.
- A tarefa serializa e desserializa para dicionário sem perda de dados.
EOF

issue "feat: implementar persistência das tarefas em arquivo JSON" "feature" "v0.2.0" <<'EOF'
Relacionado: RNF02.

**Critérios de aceite**
- Dado que não existe arquivo de dados, quando carrego, então obtenho lista vazia.
- Dado que salvei tarefas, quando reabro a aplicação, então as mesmas tarefas são carregadas.
- O caminho do arquivo pode ser definido pela variável `TASKFLOW_ARQUIVO`.
- A escrita é atômica (arquivo temporário + rename).
EOF

issue "feat: cadastrar tarefa pela CLI (taskflow adicionar)" "feature" "v0.2.0" <<'EOF'
Relacionado: RF01 · US01 · UC01.

**Critérios de aceite**
- Dado que informo um título válido, quando executo `taskflow adicionar "Estudar Git"`, então a tarefa é salva com ID sequencial e status `pendente`.
- Posso informar `--descricao`, `--prioridade` e `--prazo`.
- Dado um título vazio, então a CLI exibe mensagem de erro e retorna código 1.
EOF

issue "feat: listar e filtrar tarefas (taskflow listar)" "feature" "v0.2.0" <<'EOF'
Relacionado: RF02, RF03 · US02 · UC02.

**Critérios de aceite**
- Dado que existem tarefas, quando executo `taskflow listar`, então vejo uma tabela com ID, status, prioridade, prazo e título.
- Posso filtrar com `--status pendente|concluida` e `--prioridade baixa|media|alta`.
- Dado que não existem tarefas, então vejo a mensagem "Nenhuma tarefa encontrada.".
EOF

issue "feat: editar tarefa existente (taskflow editar)" "feature" "v0.3.0" <<'EOF'
Relacionado: RF04 · US03 · UC03.

**Critérios de aceite**
- Dado uma tarefa existente, quando executo `taskflow editar 1 --titulo "Novo"`, então apenas os campos informados são alterados.
- Dado um ID inexistente, então a CLI informa "Tarefa 99 não encontrada." e retorna código 1.
- Dado que nenhum campo foi informado, então a CLI informa que nada foi alterado.
EOF

issue "feat: concluir e reabrir tarefa (taskflow concluir / reabrir)" "feature" "v0.3.0" <<'EOF'
Relacionado: RF05 · US04 · UC04.

**Critérios de aceite**
- Dado uma tarefa pendente, quando executo `taskflow concluir 1`, então o status muda para `concluida` e a data de conclusão é registrada.
- Dado uma tarefa concluída, quando executo `taskflow reabrir 1`, então ela volta a `pendente`.
- Concluir uma tarefa já concluída exibe aviso sem erro.
EOF

issue "feat: remover tarefa com confirmação (taskflow remover)" "feature" "v0.3.0" <<'EOF'
Relacionado: RF06 · US05 · UC05.

**Critérios de aceite**
- Dado uma tarefa existente, quando executo `taskflow remover 1` e confirmo com `s`, então a tarefa é excluída.
- Quando respondo qualquer outra coisa, então a remoção é cancelada.
- A flag `--sim` remove sem pedir confirmação.
EOF

issue "bug: arquivo de dados JSON corrompido derruba a aplicação" "bug" "v0.3.1" <<'EOF'
**Passos para reproduzir**
1. Escreva conteúdo inválido no arquivo de dados (ex.: `{abc`).
2. Execute `taskflow listar`.

**Resultado atual:** traceback de `json.JSONDecodeError`.

**Critérios de aceite**
- Dado um arquivo corrompido, quando executo qualquer comando, então vejo mensagem amigável e código de saída 2, sem traceback.
- O arquivo original não é sobrescrito; uma cópia `.bak` é preservada.
EOF

issue "feat: buscar por palavra-chave e ordenar a listagem" "feature" "v1.0.0" <<'EOF'
Relacionado: RF07, RF08 · US06 · UC02.

**Critérios de aceite**
- Dado tarefas cadastradas, quando executo `taskflow buscar git`, então vejo as tarefas cujo título ou descrição contém "git" (sem diferenciar maiúsculas/acentos).
- `taskflow listar --ordenar prazo|prioridade|id` ordena o resultado; tarefas sem prazo vão para o final.
EOF

issue "feat: exibir resumo estatístico das tarefas (taskflow resumo)" "feature" "v1.0.0" <<'EOF'
Relacionado: RF09 · US07.

**Critérios de aceite**
- Quando executo `taskflow resumo`, então vejo total, pendentes, concluídas, atrasadas e percentual de conclusão.
- Dado que não há tarefas, então o percentual exibido é 0%.
EOF

issue "refactor: extrair formatação de saída da CLI para módulo próprio" "refactor" "v1.0.0" <<'EOF'
**Critérios de aceite**
- Funções de formatação (tabela, resumo) ficam em `taskflow/formatters.py`.
- A CLI não contém lógica de formatação de texto.
- Todos os testes existentes continuam passando sem alteração de comportamento.
EOF

issue "docs: finalizar README com badges, instalação, funcionalidades e fluxo de branches" "documentation" "v1.0.0" <<'EOF'
**Critérios de aceite**
- Título, descrição do problema e badges (versão, licença, CI).
- Tabela de funcionalidades implementadas vs. planejadas.
- Passo a passo de instalação e execução local.
- Links para todos os documentos de `docs/`.
- Tabela/diagrama do fluxo de branches (Git Flow) e convenção de commits.
EOF

issue "enhancement: exportar tarefas para CSV (taskflow exportar)" "enhancement" "v1.1.0" <<'EOF'
Relacionado: RF10 · US08. **Planejado — fora do escopo da semana.**

**Critérios de aceite**
- Quando executo `taskflow exportar tarefas.csv`, então um CSV com cabeçalho e todas as tarefas é gerado em UTF-8.
- Dado que o arquivo de destino existe, então a CLI pede confirmação antes de sobrescrever.
EOF

echo ">> Backlog criado com sucesso."
