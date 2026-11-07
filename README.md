# TaskFlow CLI

[![Versão](https://img.shields.io/badge/vers%C3%A3o-v1.0.0-blue)](https://github.com/JulianaPelozo/especificacao-gestao-SDLC/releases)
[![CI](https://github.com/JulianaPelozo/especificacao-gestao-SDLC/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/JulianaPelozo/especificacao-gestao-SDLC/actions/workflows/ci.yml)
[![Licença: MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-fe5196)](https://www.conventionalcommits.org/pt-br/v1.0.0/)

Mini-gerenciador de tarefas **de linha de comando**, escrito em Python e sem dependências externas.

## O problema

Quem passa o dia no terminal (estudantes de computação, desenvolvedores) costuma controlar as pendências em post-its, blocos de notas soltos ou ferramentas web pesadas, que pedem conta, internet e uma troca de contexto. Com isso, prazos são esquecidos e não há uma visão clara do que já foi feito.

O **TaskFlow CLI** resolve isso **dentro do terminal**: cadastre, liste, filtre, busque, edite, conclua e remova tarefas com um comando, e veja seu progresso em um resumo. Os dados ficam em um **arquivo JSON local e legível**, sem cadastro, servidor ou rede.

```
$ taskflow adicionar "Entregar relatório" --prioridade alta --prazo 2026-11-05
Tarefa 1 criada: Entregar relatório

$ taskflow listar --ordenar prioridade
ID  STATUS     PRIORIDADE  PRAZO        TÍTULO
--  ---------  ----------  -----------  ------
1   pendente   alta        2026-11-05!  Entregar relatório
2   concluida  media       2026-11-20   Revisar Programação
3   pendente   baixa       2026-11-12   Ler artigo sobre SemVer
3 tarefa(s).   (! = atrasada)

$ taskflow resumo
Resumo das tarefas
------------------
Total:       3
Pendentes:   2
Concluídas:  1
Atrasadas:   1

Progresso: [███████░░░░░░░░░░░░░] 33%
```

## Funcionalidades

| Status | Funcionalidade | Comando | Requisito | Issue | Versão |
|:---:|---|---|---|---|---|
| ✅ | Cadastrar tarefa (título, descrição, prioridade, prazo) | `adicionar` | RF01 | [#10](../../issues/10) | v0.2.0 |
| ✅ | Listar tarefas em tabela | `listar` | RF02 | [#11](../../issues/11) | v0.2.0 |
| ✅ | Filtrar por status e prioridade | `listar -s/-p` | RF03 | [#11](../../issues/11) | v0.2.0 |
| ✅ | Editar campos de uma tarefa | `editar` | RF04 | [#12](../../issues/12) | v0.3.0 |
| ✅ | Concluir e reabrir tarefa | `concluir`, `reabrir` | RF05 | [#13](../../issues/13) | v0.3.0 |
| ✅ | Remover com confirmação | `remover [--sim]` | RF06 | [#14](../../issues/14) | v0.3.0 |
| ✅ | Tratamento de arquivo de dados corrompido | — | RNF03 | [#15](../../issues/15) | v0.3.1 |
| ✅ | Buscar por palavra-chave (ignora acentos e maiúsculas) | `buscar` | RF07 | [#16](../../issues/16) | v1.0.0 |
| ✅ | Ordenar por ID, prazo ou prioridade | `listar -o` | RF08 | [#16](../../issues/16) | v1.0.0 |
| ✅ | Resumo com progresso e tarefas atrasadas | `resumo` | RF09 | [#17](../../issues/17) | v1.0.0 |
| 🗓️ | Exportar para CSV | `exportar` | RF10 | [#20](../../issues/20) | v1.1.0 (planejada) |

## Instalação e execução local

**Pré-requisitos:** [Python 3.10+](https://www.python.org/downloads/) e [Git](https://git-scm.com/).

1. **Clone o repositório**
   ```bash
   git clone https://github.com/JulianaPelozo/especificacao-gestao-SDLC.git
   cd especificacao-gestao-SDLC
   ```

2. **Crie e ative um ambiente virtual** (recomendado)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```

3. **Instale o pacote** (modo editável; cria o comando `taskflow`)
   ```bash
   pip install -e .
   ```

4. **Use**
   ```bash
   taskflow --help
   taskflow adicionar "Minha primeira tarefa"
   taskflow listar
   ```

   > Para rodar sem instalar: `PYTHONPATH=src python3 -m taskflow listar`

5. **Rode os testes**
   ```bash
   PYTHONPATH=src python3 -m unittest discover -s tests -t . -v
   ```

### Referência de comandos

| Comando | Descrição |
|---|---|
| `taskflow adicionar "<título>" [-d DESC] [-p baixa\|media\|alta] [--prazo AAAA-MM-DD]` | Cadastra uma tarefa |
| `taskflow listar [-s pendente\|concluida] [-p PRIORIDADE] [-o id\|prazo\|prioridade]` | Lista, filtra e ordena |
| `taskflow buscar <termo> [-o CRITÉRIO]` | Busca no título e na descrição |
| `taskflow editar <id> [-t TÍTULO] [-d DESC] [-p PRIORIDADE] [--prazo DATA \| --sem-prazo]` | Altera campos |
| `taskflow concluir <id>` / `taskflow reabrir <id>` | Muda o status |
| `taskflow remover <id> [--sim]` | Remove (pede confirmação, a menos que use `--sim`) |
| `taskflow resumo` | Mostra contadores e progresso |

**Arquivo de dados:** `~/.taskflow/tarefas.json`. Para usar outro caminho, defina a variável `TASKFLOW_ARQUIVO`:

```bash
TASKFLOW_ARQUIVO=./estudos.json taskflow listar
```

**Códigos de saída:** `0` sucesso · `1` erro de uso/validação (ex.: ID inexistente) · `2` erro no arquivo de dados.

