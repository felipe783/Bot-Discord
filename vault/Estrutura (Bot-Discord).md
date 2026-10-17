# Estrutura do Projeto

```text
Bot-Discord/
	📁 Comandos
	|  |--📁 Cog_ADM
	|  |  |--apagar.py            ← /apagar
	|  |  |--reload.py            ← /reload
	|  |--📁 Cog_normal
	|  |  |--ajuda.py             ← /ajuda
	|  |  |--buscar_mod.py        ← /busca_mod
	|  |  |--ping.py              ← /ping
	|  |  |--📁 Groups
	|  |     |--📁 Blackjack      ← /blackjack ...
	|  |     |  |--blackjack_group.py
	|  |     |  |--iniciar.py / hit.py / stand.py / double_down.py
	|  |     |--📁 Historia       ← /historia ...
	|  |        |--historia_group.py
	|  |        |--historia.py / ver_historia.py
	|  |--📁 Cogs_channel
	|  |  |--canal_comandos.py    ← cria #comandos-bot-teste
	|  |  |--canal_historia.py    ← cria #historias
	|  |--load_groups.py          ← adiciona os command groups à árvore
	📁 Estados
	|  |--estados_Blackjack.py    ← jogos = {} (estado em memória)
	📁 Json
	|  |--Data.json               ← história, ID do canal (versionado)
	📁 vault                      ← esta documentação (Obsidian); índice em _Bot-Discord
	|--main.py                    ← ponto de entrada
	|--loader.py                  ← load_db / save_db
	|--requirements.txt
	|--Dockerfile
	|--.env                       ← DISCORD_TOKEN (não versionado)
	|--README.md
```
## Pastas

- `main.py`, `loader.py`, `Comandos/load_groups.py`: ver [[!Modulo Core (Bot-Discord)]].
- `Comandos/Cog_normal/*.py`, `Comandos/Cog_ADM/`: ver [[!Modulo Comandos (Bot-Discord)]].
- `Comandos/Cog_normal/Groups/Historia/`: ver [[!Modulo História (Bot-Discord)]].
- `Comandos/Cog_normal/Groups/Blackjack/`, `Estados/`: ver [[!Modulo Blackjack]].
- `Comandos/Cogs_channel/`: ver [[!Modulo Canais (Bot-Discord)]].
- `Dockerfile`: ver [[Docker (Bot-Discord)]].
