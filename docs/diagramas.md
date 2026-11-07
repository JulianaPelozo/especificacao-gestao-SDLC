# Diagramas de Engenharia — TaskFlow CLI

Os diagramas usam [Mermaid](https://mermaid.js.org/), que o GitHub desenha direto no navegador.

## 1. Diagrama de classes

```mermaid
classDiagram
    direction LR

    class Prioridade {
        <<enumeration>>
        BAIXA = "baixa"
        MEDIA = "media"
        ALTA = "alta"
        +peso() int
    }

    class Status {
        <<enumeration>>
        PENDENTE = "pendente"
        CONCLUIDA = "concluida"
    }

    class Tarefa {
        +int id
        +str titulo
        +str descricao
        +Prioridade prioridade
        +date|None prazo
        +Status status
        +datetime criada_em
        +datetime|None concluida_em
        +concluir(agora) bool
        +reabrir() bool
        +esta_atrasada(hoje) bool
        +to_dict() dict
        +from_dict(dados)$ Tarefa
    }

    class RepositorioJSON {
        +Path caminho
        +carregar() list~Tarefa~
        +salvar(tarefas) None
    }

    class TaskService {
        -RepositorioJSON repositorio
        -Callable relogio
        +adicionar(titulo, descricao, prioridade, prazo) Tarefa
        +listar(status, prioridade, ordenar) list~Tarefa~
        +obter(id) Tarefa
        +editar(id, **campos) Tarefa
        +concluir(id) bool
        +reabrir(id) bool
        +remover(id) Tarefa
        +buscar(termo) list~Tarefa~
        +resumo() Resumo
    }

    class Resumo {
        +int total
        +int pendentes
        +int concluidas
        +int atrasadas
        +percentual() int
    }

    class cli {
        <<module>>
        +build_parser() ArgumentParser
        +main(argv) int
    }

    class formatters {
        <<module>>
        +formatar_tabela(tarefas, hoje) str
        +formatar_resumo(resumo) str
    }

    Tarefa --> Prioridade
    Tarefa --> Status
    RepositorioJSON ..> Tarefa : serializa
    TaskService --> RepositorioJSON
    TaskService ..> Tarefa : gerencia
    TaskService ..> Resumo : cria
    cli --> TaskService
    cli ..> formatters
```

**Exceções do domínio:** `ValidacaoError` (dados inválidos → código 1), `TarefaNaoEncontradaError` (ID inexistente → código 1) e `ArquivoCorrompidoError` / `RepositorioError` (problemas no arquivo → código 2).

