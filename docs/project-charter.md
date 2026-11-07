# Termo de Abertura do Projeto (Project Charter) — TaskFlow CLI

| Campo | Valor |
|---|---|
| Projeto | TaskFlow CLI — mini-gerenciador de tarefas de linha de comando |
| Responsável | Juliana Pelozo Pacheco |
| Data de abertura | 07/11/2026 |
| Duração planejada | 1 semana (07/11/2026 a 14/11/2026) |
| Versão do documento | 1.0 |

## 1. Justificativa

Estudantes e desenvolvedores costumam controlar suas pendências em post-its, blocos de notas soltos ou ferramentas web pesadas, que exigem conta, conexão com a internet e trocar de contexto, saindo do terminal. Isso leva a esquecer prazos e a não ter uma visão clara do que já foi concluído.

Uma ferramenta de linha de comando, leve e local, resolve o problema onde essas pessoas já trabalham: no terminal. Sem cadastro, sem servidor e com os dados em um arquivo legível (JSON) que pode até ser versionado.

O projeto também serve como **exercício de engenharia de software**: especificação formal, rastreabilidade de requisitos até o código e um fluxo de versionamento profissional (Git Flow, Conventional Commits e SemVer).

## 2. Visão geral do produto

O **TaskFlow CLI** é uma aplicação Python executada pelo terminal que permite **cadastrar, listar, filtrar, buscar, editar, concluir, reabrir e remover tarefas**, além de exibir um **resumo do progresso**. Cada tarefa tem título, descrição opcional, prioridade (baixa/média/alta), prazo opcional e status (pendente/concluída).

```
$ taskflow adicionar "Entregar atividade de SDLC" --prioridade alta --prazo 2026-11-14
Tarefa 1 criada: Entregar atividade de SDLC

$ taskflow listar
ID  STATUS     PRIORIDADE  PRAZO       TÍTULO
1   pendente   alta        2026-11-14  Entregar atividade de SDLC
```

## 3. Objetivos SMART

| # | Objetivo | Específico | Mensurável | Atingível | Relevante | Temporal |
|---|---|---|---|---|---|---|
| OBJ1 | Entregar o CRUD completo de tarefas via CLI | Comandos adicionar, listar, editar, concluir/reabrir e remover | 100% dos RF01–RF06 implementados e cobertos por testes | Escopo pequeno, só com a biblioteca padrão do Python | É o núcleo do valor do produto | Até 12/11/2026 (v0.3.0) |
| OBJ2 | Garantir que os dados persistam de forma confiável | Persistência em arquivo JSON com escrita atômica | 0 perdas de dados nos testes de reabertura; arquivo corrompido não gera traceback | Uso de `json` + `os.replace` | Confiança do usuário nos dados | Até 12/11/2026 (v0.3.1) |
| OBJ3 | Manter qualidade verificável | Suíte automatizada no GitHub Actions | ≥ 30 testes passando em Python 3.10 e 3.12 | `unittest` nativo, sem dependências | Evita regressões a cada issue | Contínuo, verificado em cada merge |
| OBJ4 | Garantir rastreabilidade de ponta a ponta | Todo RF ligado a UC, US, issue e commit | 100% dos commits seguindo Conventional Commits com referência `(#N)` | Convenção documentada no README | Objetivo pedagógico central | Até 14/11/2026 (v1.0.0) |
| OBJ5 | Ser rápido e fácil de usar | Respostas imediatas e mensagens em português | Qualquer comando em < 200 ms com 1.000 tarefas; `--help` em todos os comandos | Volume de dados pequeno | Ferramenta de uso diário | Até 14/11/2026 (v1.0.0) |

