# Sobre o Arquivo

O arquivo `main.py` é o **Ponto de Entrada do Bot**: configura os intents, carrega os comandos, agenda a publicação diária da história e conecta ao Discord.

Responsabilidades:
- ler `DISCORD_TOKEN` e `DISCORD_GUILD_ID` do `.env`;
- definir a subclasse `Teste(commands.Bot)`;
- registrar a tarefa `Historias_diaria` e o evento `on_ready`.
# Funcionalidades

## Classe Teste

````python
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
super().__init__(command_prefix="!", intents=intents)
````

- `message_content` é um intent **privilegiado**: precisa estar ligado no Developer Portal, mesmo que o bot só use slash commands.
- O prefixo `!` existe, mas nenhum comando de prefixo é definido.

## setup_hook

Carrega cada `.py` de `Comandos/` como extensão, chama `load_all_groups` e faz `tree.sync()` global. Ver [[Carregamento de Cogs e Groups]].

> Um bloco comentado no início limpa todos os comandos do servidor (`tree.clear_commands` + `sync` + `close`). Ele serve para remover comandos antigos que ficaram registrados.

## Historias_diaria

````python
@tasks.loop(minutes=1)
async def Historias_diaria():
    agora = datetime.now(pytz.timezone("America/Sao_Paulo"))
    if agora.hour == 12 and agora.minute == 00:
        ...  # publica e zera a história
````

Detalhes em [[História Colaborativa]].

## on_ready

Inicia `Historias_diaria` e envia "O Monstro Chegou🔥😎" a um canal de ID fixo.

> [!warning] Observações
> - `GUILD_ID = os.getenv("DISCORD_GUILD_ID")` só é usado no bloco comentado de limpeza (como texto, sem `int(...)`); o ID do canal de início está fixo no código.
> - `Historias_diaria.start()` sem `is_running()`: uma reconexão dispara `on_ready` de novo e lança `RuntimeError`.
> - `DB = load_db()` na importação usa `DB["ID_Historia"][0]`: se o canal de histórias ainda não foi criado, a lista está vazia e a tarefa falha (o erro só aparece no console).
