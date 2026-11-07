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

