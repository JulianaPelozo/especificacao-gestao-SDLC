# Especificação de Requisitos — TaskFlow CLI

Este documento lista os requisitos do TaskFlow CLI. Cada requisito tem um identificador único e estável (`RFxx` / `RNFxx`), citado nos casos de uso ([casos-de-uso.md](casos-de-uso.md)), nas histórias de usuário ([user-stories.md](user-stories.md)), nas issues do GitHub e nas mensagens de commit.

**Prioridade (MoSCoW):** **M** = Must (obrigatório) · **S** = Should (importante) · **C** = Could (desejável) · **W** = Won't (não nesta versão).

## 1. Requisitos Funcionais (RF)

| ID | Requisito | Prioridade | Versão |
|---|---|---|---|
| **[RF01]** | O sistema deve permitir **cadastrar uma tarefa** informando título (obrigatório, 1–120 caracteres), descrição (opcional), prioridade (`baixa`, `media` ou `alta`; padrão `media`) e prazo (opcional, formato `AAAA-MM-DD`). A tarefa recebe um ID inteiro sequencial, status `pendente` e data de criação. | M | v0.2.0 |
| **[RF02]** | O sistema deve permitir **listar as tarefas** em formato de tabela, exibindo ID, status, prioridade, prazo e título. | M | v0.2.0 |
| **[RF03]** | O sistema deve permitir **filtrar a listagem** por status (`pendente`/`concluida`) e por prioridade. | S | v0.2.0 |
| **[RF04]** | O sistema deve permitir **editar** título, descrição, prioridade e prazo de uma tarefa existente, alterando apenas os campos informados. O prazo pode ser removido. | M | v0.3.0 |
| **[RF05]** | O sistema deve permitir **concluir** uma tarefa (registrando a data de conclusão) e **reabrir** uma tarefa concluída. | M | v0.3.0 |
| **[RF06]** | O sistema deve permitir **remover** uma tarefa pelo ID, pedindo confirmação, a menos que o usuário use a opção `--sim`. | M | v0.3.0 |
| **[RF07]** | O sistema deve permitir **buscar tarefas por palavra-chave** no título e na descrição, sem diferenciar maiúsculas/minúsculas nem acentos. | S | v1.0.0 |
| **[RF08]** | O sistema deve permitir **ordenar a listagem** por ID, prazo (tarefas sem prazo por último) ou prioridade (alta → baixa). | C | v1.0.0 |
| **[RF09]** | O sistema deve exibir um **resumo** com total de tarefas, pendentes, concluídas, atrasadas (pendentes com prazo vencido) e percentual de conclusão. | S | v1.0.0 |
| **[RF10]** | O sistema deve permitir **exportar** as tarefas para um arquivo CSV. | W | v1.1.0 (planejado) |

## 2. Requisitos Não Funcionais (RNF)

| ID | Categoria | Requisito | Como verificar |
|---|---|---|---|
| **[RNF01]** | Desempenho | Qualquer comando deve responder em **menos de 200 ms** com até 1.000 tarefas cadastradas, em um computador comum. | Teste manual com arquivo gerado de 1.000 tarefas |
| **[RNF02]** | Persistência | As tarefas devem ser salvas em um **arquivo JSON local** (UTF-8, indentado, legível). O caminho padrão é `~/.taskflow/tarefas.json` e pode ser alterado pela variável de ambiente `TASKFLOW_ARQUIVO`. | Testes de `repository.py` |
| **[RNF03]** | Confiabilidade | A gravação deve ser **atômica** (arquivo temporário + `os.replace`), para não corromper os dados se o processo for interrompido. Um arquivo corrompido não deve gerar *traceback*: deve exibir mensagem clara, retornar código 2 e preservar uma cópia `.bak`. | Testes de `repository.py` e `cli.py` |
| **[RNF04]** | Usabilidade | Todas as mensagens devem estar em **português**; todo comando deve ter `--help`; erros devem ser explicados em uma linha, sem jargão técnico. | Revisão + testes da CLI |
| **[RNF05]** | Integridade | Dados de entrada devem ser **validados** antes da gravação (título não vazio, prioridade válida, data válida). Entradas inválidas nunca alteram o arquivo. | Testes de `models.py` |
| **[RNF06]** | Segurança | A aplicação não deve fazer **nenhum acesso à rede** nem executar conteúdo do arquivo de dados (usa só `json.load`, nunca `eval`/`pickle`). O arquivo é criado apenas no diretório do usuário. | Revisão de código |
| **[RNF07]** | Portabilidade | Deve funcionar em **Linux, macOS e Windows** com Python ≥ 3.10, usando apenas a biblioteca padrão. | CI em 3.10 e 3.12; uso de `pathlib` |
| **[RNF08]** | Manutenibilidade | Código organizado em camadas (modelo, repositório, serviço, CLI, formatação), com **testes automatizados** executados no GitHub Actions a cada push/PR. | Workflow `ci.yml` |
| **[RNF09]** | Interoperabilidade | Códigos de saída padronizados: `0` sucesso, `1` erro de uso/validação, `2` erro de dados. Isso permite usar a ferramenta em scripts. | Testes da CLI |

