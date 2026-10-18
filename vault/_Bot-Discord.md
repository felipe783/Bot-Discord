---
Tipo: projeto
Projeto: Bot-Discord
Status: ativo
Stack:
  - Python
  - discord.py
  - requests
  - pytz
  - Docker
Codigo: "Bot-Discord"
Repositorio: "https://github.com/felipe783/Bot-Discord"
Atualizado: 2026-10-17
---
# Bot-Discord

Bot de Discord em **Python (discord.py)** para um servidor específico, com **slash commands** organizados em *cogs* e *command groups*: uma **história colaborativa** que os membros escrevem frase a frase e que é publicada e zerada todo dia ao meio-dia, um **Blackjack** em que a aposta é o tempo de *timeout* de quem perde, uma **busca de mods** na API do Modrinth e comandos de administração.

- **Código:** raiz deste repositório; a documentação fica em `vault/`
- **Entrada:** interações de slash command no Discord (gateway via `bot.run(TOKEN)`)
- **Saída:** respostas e embeds no Discord, *timeouts* de membros, canais criados no servidor e o arquivo `Json/Data.json` (história e ID do canal)
- **Hospedagem:** container Docker num Ubuntu Server 24.04 (segundo o README original)

## Status

| Funcionalidade | Estado |
|---|---|
| Carregamento automático de cogs e command groups ([[BD-RF 01]]) | Implementado |
| `/ping` e `/ajuda` ([[BD-RF 02]]) | Implementado; o texto do `/ajuda` cita nomes de comando antigos |
| `/busca_mod` na API do Modrinth ([[BD-RF 03]]) | Implementado (primeiro resultado da busca) |
| História colaborativa: `/historia escrever`, `/historia ver_historia`, publicação diária ([[BD-RF 04]]) | Implementado |
| Blackjack: `/blackjack iniciar | hit | stand | double_down` com *timeout* como aposta ([[BD-RF 05]]) | Implementado |
| Comandos ADM `/apagar` e `/reload` ([[BD-RF 06]]) | Implementado; `/reload` tem defeitos (ver abaixo) |
| Criação dos canais `historias` e `comandos-bot-teste` | Implementado |
| Configuração por variáveis de ambiente | Parcial: `DISCORD_TOKEN`, e `DISCORD_GUILD_ID` só no bloco comentado de limpeza do `main.py`; cargo, canais e o servidor dos cogs de canais estão fixos no código |
| Testes automatizados | Inexistentes |

## Como rodar

```powershell
# na raiz do repositório
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# .env na raiz (não versionado)
#   DISCORD_TOKEN=<token do bot>
python main.py
```

```bash
# Docker
docker build -t bot-discord .
docker run -d --name bot-discord --env-file .env --restart unless-stopped bot-discord
```

> Os caminhos (`Comandos/`, `Json/Data.json`) são **relativos ao diretório atual**: rode `main.py` a partir da raiz.
> Em 2026-10-17 foi verificado apenas que os 26 arquivos `.py` **compilam sem erro de sintaxe**. O bot não foi executado (exige o token e conecta ao servidor real).

## Mapa das notas

- [[Visão Geral (Bot-Discord)]]: o que o bot faz e para quem.
- [[Arquitetura (Bot-Discord)]]: inicialização, carregamento de cogs/groups e tarefa diária.
- [[Resumo Principal (Bot-Discord)]]: lista de comandos e fluxos.
- [[Estrutura (Bot-Discord)]]: árvore de pastas.
- [[Dependencias (Bot-Discord)]]: bibliotecas e instalação.
- Requisitos: [[BD-RF 01]] · [[BD-RF 02]] · [[BD-RF 03]] · [[BD-RF 04]] · [[BD-RF 05]] · [[BD-RF 06]]
- Módulos:
  - [[!Modulo Core (Bot-Discord)]]: [[Main e Bot]], [[Carregamento de Cogs e Groups]], [[Loader e Data.json]].
  - [[!Modulo Comandos (Bot-Discord)]]: [[Comandos Gerais]], [[Comandos ADM]].
  - História: [[História Colaborativa]].
  - Blackjack: [[Regras do Blackjack]].
  - Canais: [[Criação de Canais]].
  - [[Docker (Bot-Discord)]].

## Problemas conhecidos

Encontrados lendo o código em 2026-10-17. Nada foi executado além da verificação de sintaxe.

- **Token dentro da imagem Docker**: não há `.dockerignore` e o `Dockerfile` faz `COPY . .`, então o `.env` (com o `DISCORD_TOKEN`) e o `.git` entram na imagem. Qualquer um com acesso à imagem lê o token.
- **`Json/Data.json` é versionado** e, no container, gravado **sem volume**: a história e o ID do canal se perdem ao recriar o container e voltam ao estado do Git.
- **IDs fixos no código**: servidor (`canal_comandos.py`, `canal_historia.py`), cargo ADM (`apagar.py`, `canal_comandos.py`) e canais (`main.py`, `reload.py`). O `main.py` lê `DISCORD_GUILD_ID` do `.env` desde o commit `72c1e09`, mas só o usa no bloco comentado que limpa os comandos.
- **`/reload`**: chama `send_message` dentro do laço (a segunda resposta lança `InteractionResponded`), usa `reload_extension` em módulos que podem não estar carregados e não recarrega os command groups nem faz `tree.sync()`.
- **`on_ready` chama `Historias_diaria.start()`** sem verificar se já está rodando: numa reconexão do gateway o `on_ready` dispara de novo e a tarefa lança `RuntimeError`.
- **Publicação diária frágil**: o loop roda a cada 1 minuto e só age se o horário for exatamente `12:00`. Se o bot estiver fora do ar nesse minuto, a história não é publicada naquele dia.
- **`load_db()` devolve `[]`** quando o JSON não existe, mas o código usa o retorno como `dict` (`DB["ID_Historia"]`, `db.get(...)`). Sem o arquivo, o bot quebra na importação de `main.py`.
- **Escritas concorrentes no JSON**: `/historia escrever`, a tarefa diária e `/apagar` fazem *load → modifica → save* sem trava; duas chamadas simultâneas podem perder uma frase.
- **Timeout no Blackjack**: `interaction.user.timeout(...)` falha (`Forbidden`) para administradores/dono ou sem a permissão *Moderate Members*, depois da resposta já enviada; o erro não é tratado.
- **`/busca_mod`** usa `requests` (bloqueante, sem `timeout`) dentro de uma corrotina: uma API lenta trava o bot inteiro.
- **`/apagar`**: `db("historia:", [])` chama o dicionário como função (só executa se o JSON não for `dict`) e usa o ID do canal lido na importação do módulo.
- **Regras do Blackjack**: no `hit`, o dealer recebe uma carta a cada compra do jogador; no `double_down`, o dealer compra só 1 carta e não vai até 17. Ver [[Regras do Blackjack]].
- Funções `formatar_mao` e `calcular_pontos` duplicadas nos 4 arquivos do Blackjack; `nest_asyncio` está no `requirements.txt` mas não é usado; os `__all__` dos pacotes estão desatualizados.
- O README original citava `/buscar_mod`, `/historia {texto}` e `/ver historia`; os nomes reais são `/busca_mod`, `/historia escrever` e `/historia ver_historia`.

## Decisões

- **Slash commands (`app_commands`)** em vez de prefixo `!`: autocompletar e permissões nativas do Discord.
- **Cogs por pasta**: `main.py` carrega como extensão todo `.py` de `Comandos/` (exceto `_*`), então um comando novo não precisa ser registrado à mão.
- **Command groups por convenção**: cada pasta em `Comandos/Cog_normal/Groups/<Nome>` exporta `<nome>_group`, e `__load_groups.py` o adiciona à árvore de comandos.
- **Persistência em JSON** (`Json/Data.json`) em vez de banco: suficiente para uma lista de frases e um ID de canal.
- **Estado do Blackjack em memória** (`Estados/estados_Blackjack.py`, `dict` por `user_id`): partidas não sobrevivem a reinícios, o que é aceitável para um jogo curto.

## Próximos passos sugeridos

1. Criar `.dockerignore` (`.env`, `.git`, `__pycache__`) e passar o token com `docker run --env-file .env`; montar `Json/` como volume.
2. Ler servidor, cargo e canais de variáveis de ambiente (usar o `DISCORD_GUILD_ID` que já existe).
3. Corrigir o `/reload` (uma resposta só, `defer` + `followup`) e proteger `Historias_diaria.start()` com `is_running()`.
4. Trocar a condição `hour == 12 and minute == 0` por `@tasks.loop(time=datetime.time(12, tzinfo=...))`.
5. Usar `aiohttp` (que já vem com o discord.py) no `/busca_mod`, com timeout.
6. Extrair as funções do Blackjack para um módulo único e adicionar testes de `calcular_pontos`.
