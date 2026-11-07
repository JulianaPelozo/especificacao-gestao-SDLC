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

## US03 — Editar tarefa

> **Como** usuário,
> **quero** alterar o título, a descrição, a prioridade ou o prazo de uma tarefa
> **para que** ela continue certa quando os planos mudarem.

```gherkin
Funcionalidade: Editar tarefa

  Cenário: Alterar só a prioridade
    Dado que existe a tarefa 1 "Estudar Git" com prioridade "alta"
    Quando executo taskflow editar 1 --prioridade baixa
    Então vejo a mensagem "Tarefa 1 atualizada."
    E a tarefa 1 tem prioridade "baixa" e o título continua "Estudar Git"

  Cenário: Remover o prazo
    Dado que a tarefa 1 tem prazo 2026-11-10
    Quando executo taskflow editar 1 --sem-prazo
    Então a tarefa 1 fica sem prazo

  Cenário: Tarefa inexistente
    Quando executo taskflow editar 99 --titulo "X"
    Então vejo a mensagem "Erro: Tarefa 99 não encontrada."
    E o código de saída é 1

  Cenário: Nenhum campo informado
    Quando executo taskflow editar 1
    Então vejo uma mensagem informando que não há nada para alterar
```

---

## US04 — Concluir e reabrir tarefa

> **Como** usuário,
> **quero** marcar uma tarefa como concluída e, se precisar, reabri-la
> **para que** eu acompanhe o que já foi feito sem perder o histórico.

```gherkin
Funcionalidade: Concluir e reabrir tarefa

  Cenário: Concluir tarefa pendente
    Dado que a tarefa 1 está "pendente"
    Quando executo taskflow concluir 1
    Então vejo a mensagem "Tarefa 1 concluída."
    E a tarefa 1 fica com status "concluida" e data de conclusão registrada

  Cenário: Concluir tarefa já concluída
    Dado que a tarefa 1 está "concluida"
    Quando executo taskflow concluir 1
    Então vejo o aviso "Tarefa 1 já estava concluída."
    E o código de saída é 0

  Cenário: Reabrir tarefa
    Dado que a tarefa 1 está "concluida"
    Quando executo taskflow reabrir 1
    Então a tarefa 1 volta a "pendente" e fica sem data de conclusão
```

---

## US05 — Remover tarefa

> **Como** usuário,
> **quero** remover uma tarefa que não faz mais sentido, com uma confirmação antes
> **para que** minha lista fique limpa sem o risco de apagar algo por engano.

```gherkin
Funcionalidade: Remover tarefa

  Cenário: Remover confirmando
    Dado que existe a tarefa 1
    Quando executo taskflow remover 1
    E respondo "s" à confirmação
    Então vejo a mensagem "Tarefa 1 removida."
    E a tarefa 1 não aparece mais na listagem

  Cenário: Cancelar a remoção
    Quando executo taskflow remover 1
    E respondo "n" à confirmação
    Então vejo a mensagem "Remoção cancelada."
    E a tarefa 1 continua existindo

  Cenário: Remover sem confirmação (scripts)
    Quando executo taskflow remover 1 --sim
    Então a tarefa 1 é removida sem nenhuma pergunta
```

---

