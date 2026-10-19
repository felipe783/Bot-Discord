# CLAUDE.md — Bot-Discord

Bot de Discord em **Python (discord.py)**, para um servidor específico, com slash commands em *cogs* e *command groups*: **história colaborativa** (publicada e zerada todo dia às 12:00 de São Paulo), **Blackjack** em que a aposta é o tempo de *timeout* de quem perde, **busca de mods** no Modrinth e comandos ADM. A persistência é `Json/Data.json`. Roda em Docker num Ubuntu Server.

O perfil do autor e as preferências gerais estão no `CLAUDE.md` de `!Faculdade`. Este arquivo trata só do que é específico deste repositório.

## Documentação (fonte de verdade)

O índice abaixo é carregado em toda sessão. As notas detalhadas ficam em `vault/` e devem ser lidas **sob demanda**:

@vault/_Bot-Discord.md

| Assunto | Nota |
|---|---|
| Inicialização, carregamento e tarefa diária | `vault/Arquitetura (Bot-Discord).md` |
| `main.py`, intents, `on_ready` | `vault/modulos/Core/Main e Bot.md` |
| Como um arquivo vira comando / group | `vault/modulos/Core/Carregamento de Cogs e Groups.md` |
| `load_db` / `save_db` e formato do JSON | `vault/modulos/Core/Loader e Data.json.md` |
| `/ping`, `/ajuda`, `/busca_mod`, `/apagar`, `/reload` | `vault/modulos/Comandos/` |
| História colaborativa | `vault/modulos/Historia/História Colaborativa.md` |
| Regras do Blackjack | `vault/modulos/Blackjack/Regras do Blackjack.md` |
| Criação de canais | `vault/modulos/Canais/Criação de Canais.md` |
| Dockerfile e riscos | `vault/modulos/Docker (Bot-Discord).md` |

Conceitos transversais (segredos, Docker, configuração, persistência em JSON…), com aprendizados deste e de outros projetos: `../Contexto-Projetos/Conhecimento/_Conhecimento.md`. Leia sob demanda, quando a tarefa tocar o assunto.

## Mapa do código

- `main.py`: classe `Teste(commands.Bot)`, `setup_hook` (carrega cogs e groups, `tree.sync()`), tarefa `Historias_diaria` e `on_ready`.
- `loader.py`: `load_db()` / `save_db()` sobre `Json/Data.json` (caminho relativo ao diretório atual).
- `Comandos/Cog_normal/`: `ping.py`, `ajuda.py`, `buscar_mod.py` (o comando é **`/busca_mod`**).
- `Comandos/Cog_ADM/`: `apagar.py`, `reload.py`.
- `Comandos/Cogs_channel/`: criam `#historias` e `#comandos-bot-teste` no primeiro `on_ready`.
- `Comandos/Cog_normal/Groups/<Nome>/`: command groups (`Blackjack`, `Historia`). O `__init__.py` importa `<nome>_group` e os subcomandos.
- `Comandos/__load_groups.py`: adiciona os groups à árvore. O `_` no início impede que seja carregado como extensão.
- `Estados/estados_Blackjack.py`: `jogos = {}`, o estado das mesas **em memória**, por `user_id`.

## Comandos

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py                      # sempre a partir da raiz

# verificação sem conectar ao Discord (só sintaxe)
python -c "import ast,pathlib; [ast.parse(p.read_text(encoding='utf-8')) for p in pathlib.Path('.').rglob('*.py') if '.venv' not in p.parts]; print('ok')"
```

```bash
docker build -t bot-discord .
docker run -d --name bot-discord --env-file .env --restart unless-stopped bot-discord
docker logs -f bot-discord
```

Não há testes automatizados; o que já foi verificado, e quando, está no "Como rodar" do índice.

## Regras deste projeto

- **Não execute o bot** (`python main.py`, `docker run`) sem pedido explícito: ele conecta ao servidor **real**, envia mensagem no canal de início e, ao meio-dia, publica a história com `@everyone`.
- **Segredos**: nunca exiba nem copie o valor de `DISCORD_TOKEN` (`.env`). Não faça build/push de imagem sem `.dockerignore`: o `COPY . .` leva o `.env` para dentro dela.
- **`Json/Data.json` é estado real** (frases da história, ID do canal) e é versionado. Não sobrescreva nem limpe sem pedir; para testar, use uma cópia.
- **Comando novo** = arquivo `.py` em `Comandos/` com `async def setup(bot)` e um `commands.Cog`. Ele é carregado automaticamente, sem registro manual.
- **Subcomando de grupo** = arquivo na pasta do grupo com `@<nome>_group.command(...)` e um `async def setup(bot): pass`. **Grupo novo** = pasta `Groups/<Nome>/` com `<nome>_group.py` (`app_commands.Group`) e o `__init__.py` no mesmo padrão dos existentes.
- Arquivos que **não** devem virar extensão começam com `_`.
- IDs de servidor, cargo ADM e canais estão fixos no código (`main.py`, `Cog_ADM/`, `Cogs_channel/`). O `main.py` lê `DISCORD_GUILD_ID`, mas só o usa no bloco comentado de limpeza. Ao mexer nisso, prefira ler do `.env`.
- Escritas no JSON são *load → modifica → save*, sem trava. Não adicione escritas concorrentes sem considerar isso.
- Textos de resposta seguem o tom do bot (informal, com emojis); nomes em português.

## Armadilhas conhecidas

Estão em **Problemas conhecidos** do índice importado acima (`vault/_Bot-Discord.md`), que é a única lista mantida.

## Manter a documentação

Ao alterar comportamento, atualize na mesma tarefa:
1. `vault/_Bot-Discord.md`: **Status**, **Problemas conhecidos** e `Atualizado` no frontmatter.
2. A nota do módulo afetado (tabela acima).
3. O `README.md`, se mudar comando, permissão, variável de ambiente ou forma de rodar.

Convenções do vault (o mesmo do Obsidian em `Contexto-Projetos/Bot-Discord`, via junction):
- Frontmatter: siga a tabela de **Convenções** em `../Contexto-Projetos/Contexto Geral.md`, que é a única definição (`Tipo`, `Status` controlado, `Codigo` relativo) e tem templates em `_templates/`.
- Nomes de nota únicos no vault inteiro: notas genéricas levam `(Bot-Discord)`; requisitos usam `BD-RF NN`.
- Links `[[Nome da Nota]]`. Separe o que foi **executado** do que foi **lido no código**, com data.
