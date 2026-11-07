# Especificação de Casos de Uso — TaskFlow CLI

## 1. Atores

| Ator | Tipo | Descrição |
|---|---|---|
| **Usuário** | Primário (humano) | Pessoa que usa o terminal para organizar suas tarefas. Inicia todos os casos de uso. |
| **Script / automação** | Primário (sistema) | Script de shell ou agendador que chama o `taskflow` sem interação (ex.: `--sim`) e lê os códigos de saída. |
| **Sistema de arquivos** | Secundário (sistema) | Armazena o arquivo JSON de dados. Pode estar indisponível, sem permissão ou com conteúdo inválido. |

## 2. Diagrama de casos de uso

```mermaid
flowchart LR
    U([Usuário])
    S([Script / automação])
    FS[(Sistema de arquivos)]
    subgraph TaskFlow CLI
        UC01((UC01 Cadastrar tarefa))
        UC02((UC02 Listar tarefas))
        UC03((UC03 Editar tarefa))
        UC04((UC04 Concluir / reabrir))
        UC05((UC05 Remover tarefa))
        UC06((UC06 Buscar tarefas))
        UC07((UC07 Ver resumo))
    end
    U --- UC01 & UC02 & UC03 & UC04 & UC05 & UC06 & UC07
    S --- UC01 & UC02 & UC05
    UC01 & UC02 & UC03 & UC04 & UC05 & UC06 & UC07 --- FS
```

## 3. Pré-condição comum

Em todos os casos de uso, o sistema carrega o arquivo de dados antes de executar a operação.

- **Exceção comum E-ARQ (arquivo corrompido):** se o arquivo existe mas não é um JSON válido, o sistema copia o arquivo para `<arquivo>.bak`, exibe *"Erro: o arquivo de dados está corrompido. Uma cópia foi salva em …"*, **não altera o arquivo** e encerra com código 2.
- **Exceção comum E-PERM (sem permissão):** se não for possível ler ou gravar o arquivo, o sistema exibe *"Erro: não foi possível acessar o arquivo de dados: …"* e encerra com código 2.

---

## UC01 — Cadastrar tarefa

| | |
|---|---|
| **Requisitos** | RF01, RNF02, RNF03, RNF05 |
| **Ator primário** | Usuário ou script |
| **Pré-condições** | Nenhuma além da pré-condição comum. |
| **Pós-condições** | Uma nova tarefa `pendente` está salva no arquivo, com ID único. |

**Fluxo principal**
1. O usuário executa `taskflow adicionar "<título>"` com opções `--descricao`, `--prioridade` e `--prazo`.
2. O sistema remove os espaços das pontas e valida os dados (RN04, RNF05).
3. O sistema gera o próximo ID (RN01) e registra a data de criação.
4. O sistema grava o arquivo de forma atômica.
5. O sistema exibe *"Tarefa N criada: <título>"* e encerra com código 0.

**Fluxos alternativos**
- **A1 — Sem prioridade informada:** no passo 2, a prioridade padrão `media` é usada.
- **A2 — Primeiro uso:** no passo 4, se o diretório `~/.taskflow/` não existe, ele é criado.

**Fluxos de exceção**
- **E1 — Título vazio:** no passo 2, o sistema exibe *"Erro: o título não pode ser vazio."* e encerra com código 1, sem gravar.
- **E2 — Prazo inválido:** no passo 2, se o prazo não está no formato `AAAA-MM-DD`, o sistema exibe *"Erro: prazo inválido …"* e encerra com código 1.
- **E3 — Prioridade inválida:** o `argparse` rejeita o valor e lista as opções válidas (código 2 do argparse).

---

## UC02 — Listar tarefas

| | |
|---|---|
| **Requisitos** | RF02, RF03, RF08 |
| **Ator primário** | Usuário ou script |
| **Pós-condições** | Nenhuma alteração nos dados. |

**Fluxo principal**
1. O usuário executa `taskflow listar`.
2. O sistema carrega as tarefas.
3. O sistema exibe uma tabela com ID, status, prioridade, prazo e título, ordenada por ID, e encerra com código 0.

**Fluxos alternativos**
- **A1 — Filtro por status:** com `--status pendente|concluida`, só as tarefas com aquele status são exibidas.
- **A2 — Filtro por prioridade:** com `--prioridade baixa|media|alta`, só as tarefas com aquela prioridade são exibidas. Filtros podem ser combinados.
- **A3 — Ordenação:** com `--ordenar prazo|prioridade|id`, a tabela é ordenada pelo critério escolhido; tarefas sem prazo aparecem por último.
- **A4 — Tarefas atrasadas:** tarefas atrasadas (RN02) são marcadas com `!` ao lado do prazo.

**Fluxos de exceção**
- **E1 — Nenhuma tarefa:** se a lista (após filtros) está vazia, o sistema exibe *"Nenhuma tarefa encontrada."* e encerra com código 0.

---

