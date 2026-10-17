# Bot Teste🔥

Bot de Discord em **Python (discord.py)** com slash commands: uma **história colaborativa** que o servidor escreve junto e que é publicada todo dia ao meio-dia, um **Blackjack** em que a aposta é o tempo de *timeout* de quem perde, uma **busca de mods** no Modrinth e comandos de administração.

- O bot está hospedado no meu Ubuntu Server 24.04, rodando dentro de um container Docker.

## Comandos Normais

> ***Comandos que qualquer um pode usar***

| Comando | O que faz |
|---|---|
| `/ajuda` | Mostra a lista de comandos (só para quem chamou) |
| `/ping` | O bot responde com um `pong` |
| `/busca_mod [texto]` | Busca o mod na [API do Modrinth](https://docs.modrinth.com/api/) e mostra descrição, autor, downloads e link do primeiro resultado |

### /historia

> É um **group command**

| Comando | O que faz |
|---|---|
| `/historia escrever [texto]` | Junta a sua frase à história do servidor e mostra como ela ficou |
| `/historia ver_historia` | Mostra a história atual (só para quem chamou) |

Todo dia às **12:00 (horário de Brasília)** a história inteira é enviada no canal `historias` e zerada.

### /blackjack

> É um **group command**. A aposta é em **minutos de timeout**: se perder, você fica de castigo esse tempo 😎

| Comando | O que faz |
|---|---|
| `/blackjack iniciar <aposta>` | Começa um jogo de Blackjack contra o dealer (aposta obrigatória, maior que 0) |
| `/blackjack hit` | Compra mais uma carta; pode repetir enquanto não estourar |
| `/blackjack stand` | Para de comprar; o dealer compra até 17 e quem tiver mais pontos sem estourar ganha |
| `/blackjack double_down` | Dobra a aposta, compra mais uma carta e encerra a jogada (só antes do primeiro `hit`) |

## Comandos ADM

> ***Só para administradores***. O `/apagar` ainda exige o cargo `ADM` do servidor.

| Comando | O que faz |
|---|---|
| `/apagar` | Publica e zera a história antes do horário |
| `/reload` | Recarrega os comandos sem reiniciar o bot |

## Canais criados pelo bot

Ao iniciar, o bot cria os canais de que precisa se eles ainda não existirem:
- `historias`: só o bot escreve; o ID fica salvo em `Json/Data.json`;
- `comandos-bot-teste`: visível só para o cargo ADM.

## Configuração local

Requisitos: Python 3.12 e um bot criado no [Discord Developer Portal](https://discord.com/developers/applications) com:
- **Message Content Intent** ligado (*Bot → Privileged Gateway Intents*);
- permissões **Send Messages**, **Manage Channels** e **Moderate Members** (para o timeout do Blackjack);
- convite com os escopos `bot` e `applications.commands`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz (ele está no `.gitignore` e **nunca** deve ser commitado):

```dotenv
DISCORD_TOKEN=cole_aqui_o_token_do_bot
DISCORD_GUILD_ID=id_do_seu_servidor
```

> `DISCORD_GUILD_ID` é lido pelo `main.py`, mas por enquanto só no bloco comentado que limpa os comandos. O cargo ADM, os canais e o servidor usado na criação de canais continuam **fixos no código** (`main.py`, `Comandos/Cog_ADM/`, `Comandos/Cogs_channel/`); para usar o bot em outro servidor, troque esses IDs.

## Como rodar

Rode sempre **a partir da raiz** do projeto, porque `Comandos/` e `Json/Data.json` são caminhos relativos:

```powershell
python main.py
```

No console aparecem os cogs carregados e `Comandos sincronizados (tree.sync) ✅`. Comandos novos podem levar alguns minutos para aparecer no Discord.

### Docker

```bash
docker build -t bot-discord .
docker run -d --name bot-discord --restart unless-stopped bot-discord
docker logs -f bot-discord
```

> ⚠️ Não há `.dockerignore`: o `COPY . .` leva o `.env` com o token para dentro da imagem. Não publique essa imagem. O `Json/Data.json` também fica dentro do container e se perde ao recriá-lo.

## Solução de problemas

| Sintoma | Causa provável |
|---|---|
| `Improper token has been passed` | `DISCORD_TOKEN` vazio ou errado no `.env` |
| `PrivilegedIntentsRequired` | Message Content Intent desligado no Developer Portal |
| Comandos não aparecem | Sincronização global ainda propagando, ou bot convidado sem `applications.commands` |
| `Pasta 'Comandos' não encontrada` / `Json/Data.json` não achado | Bot iniciado fora da raiz do projeto |
| Blackjack não aplica o timeout | Falta a permissão *Moderate Members*, ou o jogador é administrador/dono |

## 📚 Documentação

A documentação completa da arquitetura está em [`vault/_Bot-Discord.md`](vault/_Bot-Discord.md). Consulte esse arquivo como ponto de entrada para os comandos, o carregamento de cogs e groups, a persistência, os problemas conhecidos e os próximos passos.
