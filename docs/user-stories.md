# Histórias de Usuário — TaskFlow CLI

Formato: **"Como [ator], quero [ação] para que [valor de negócio]"**, com critérios de aceite em **Gherkin** (Dado / Quando / Então). As histórias são numeradas `USxx` e ligadas aos requisitos de [requisitos.md](requisitos.md).

| ID | História (resumo) | RF | Prioridade | Estimativa | Issue |
|---|---|---|---|---|---|
| US01 | Cadastrar tarefa | RF01 | Must | 3 pts | #10 |
| US02 | Listar e filtrar tarefas | RF02, RF03 | Must | 3 pts | #11 |
| US03 | Editar tarefa | RF04 | Must | 2 pts | #12 |
| US04 | Concluir e reabrir tarefa | RF05 | Must | 2 pts | #13 |
| US05 | Remover tarefa | RF06 | Must | 2 pts | #14 |
| US06 | Buscar e ordenar tarefas | RF07, RF08 | Should | 3 pts | #16 |
| US07 | Ver resumo do progresso | RF09 | Should | 2 pts | #17 |
| US08 | Exportar para CSV | RF10 | Won't (v1.1.0) | 2 pts | #20 |

---

## US01 — Cadastrar tarefa

> **Como** estudante que usa o terminal,
> **quero** cadastrar uma tarefa com título, prioridade e prazo
> **para que** eu não esqueça o que preciso entregar e quando.

```gherkin
Funcionalidade: Cadastrar tarefa

  Cenário: Cadastro com todos os campos
    Dado que não existem tarefas cadastradas
    Quando executo taskflow adicionar "Estudar Git" --descricao "Cap. 3" --prioridade alta --prazo 2026-11-10
    Então vejo a mensagem "Tarefa 1 criada: Estudar Git"
    E a tarefa 1 fica salva com status "pendente" e prioridade "alta"

  Cenário: Cadastro só com o título
    Quando executo taskflow adicionar "Ler artigo"
    Então a tarefa é criada com prioridade "media" e sem prazo

  Cenário: Título vazio
    Quando executo taskflow adicionar "   "
    Então vejo a mensagem "Erro: o título não pode ser vazio."
    E o código de saída é 1
    E nenhuma tarefa é gravada

  Cenário: Prazo em formato inválido
    Quando executo taskflow adicionar "Prova" --prazo 10/11/2026
    Então vejo uma mensagem de erro de prazo inválido
    E o código de saída é 1
```

---

## US02 — Listar e filtrar tarefas

> **Como** usuário,
> **quero** ver minhas tarefas em uma tabela e filtrá-las por status e prioridade
> **para que** eu saiba rapidamente o que ainda falta fazer.

```gherkin
Funcionalidade: Listar tarefas

  Contexto:
    Dado que existem as tarefas
      | id | título       | prioridade | status    |
      | 1  | Estudar Git  | alta       | pendente  |
      | 2  | Ler artigo   | baixa      | concluida |

  Cenário: Listagem completa
    Quando executo taskflow listar
    Então vejo uma tabela com as colunas ID, STATUS, PRIORIDADE, PRAZO e TÍTULO
    E vejo as tarefas 1 e 2

  Cenário: Filtrar por status
    Quando executo taskflow listar --status pendente
    Então vejo apenas a tarefa 1

  Cenário: Filtrar por prioridade
    Quando executo taskflow listar --prioridade baixa
    Então vejo apenas a tarefa 2

  Cenário: Nenhum resultado
    Quando executo taskflow listar --status pendente --prioridade baixa
    Então vejo a mensagem "Nenhuma tarefa encontrada."
```

---

