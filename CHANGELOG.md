# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.3.0] - 2026-11-10

### Adicionado
- Comando `taskflow editar` com alteração parcial e `--sem-prazo` (RF04) (#12).
- Comandos `taskflow concluir` e `taskflow reabrir` (RF05) (#13).
- Comando `taskflow remover` com confirmação interativa e `--sim` (RF06) (#14).

## [0.2.0] - 2026-11-08

### Adicionado
- Entidade `Tarefa` com validação de título, prioridade e prazo, além de serialização (#8).
- Persistência em JSON com escrita atômica e caminho configurável por `TASKFLOW_ARQUIVO` (#9).
- Comando `taskflow adicionar` (RF01) (#10).
- Comando `taskflow listar` com filtros `--status`/`--prioridade` e marcação de atraso (RF02, RF03) (#11).

## [0.1.0] - 2026-11-07

### Adicionado
- Termo de Abertura do Projeto (`docs/project-charter.md`) (#2).
- Requisitos funcionais, não funcionais, regras de negócio e matriz de rastreabilidade (`docs/requisitos.md`) (#3).
- Casos de uso UC01–UC07 com fluxos principais, alternativos e de exceção (`docs/casos-de-uso.md`) (#4).
- Histórias de usuário US01–US08 com critérios de aceite em Gherkin (`docs/user-stories.md`) (#5).
- Diagramas de classes, modelo de dados, C4 e wireframes (`docs/diagramas.md`) (#6).
- Estrutura do pacote em `src/`, `pyproject.toml`, `.gitignore`, CI no GitHub Actions e script de criação do backlog (#7).

