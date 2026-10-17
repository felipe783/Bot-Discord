# Sobre os Arquivos

`canal_historia.py` e `canal_comandos.py` são *listeners* de `on_ready` que **criam canais** se eles não existirem (com uma *flag* `_done` para rodar só uma vez por processo).
# Funcionalidades

| Cog | Canal | Permissões |
|---|---|---|
| `CanalHistoria` | `historias` | ninguém envia mensagens, exceto o bot; o ID é gravado em `Data.json["ID_Historia"]` |
| `ChannelCreator` | `comandos-bot-teste` | invisível para `@everyone`; visível e com escrita para o cargo ADM |

- O servidor e o cargo vêm de **IDs fixos** no código.
- A busca é pelo **nome** (`discord.utils.get(guild.text_channels, name=...)`): renomear o canal faz o bot criar outro.

> Exige a permissão *Manage Channels* para o bot. Se o servidor não estiver no cache (`get_guild` devolve `None`), o cog quebra com `AttributeError`.
