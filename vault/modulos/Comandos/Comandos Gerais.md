# Sobre os Arquivos

`ping.py`, `ajuda.py` e `buscar_mod.py` são os **comandos utilitários** abertos a todos.
# Funcionalidades

## /ping

Responde "PONG😎🔥".

## /ajuda

Envia dois embeds **efêmeros** (só quem chamou vê): comandos gerais (azul) e ADM (vermelho).

> O texto ainda lista `/historia`, `/ver_historia` e `/buscar_mod`. Os nomes reais são `/historia escrever`, `/historia ver_historia` e `/busca_mod`, e o Blackjack não aparece.

## /busca_mod [texto]

````python
url = "https://api.modrinth.com/v2/search"
params = {"query": texto, "limit": 5}
res = requests.get(url, params=params, headers={"User-Agent": "SeuBotDiscord/1.0"})
hits = res.json().get("hits", [])
````

- Usa o **primeiro** resultado: título, descrição (200 caracteres + "..."), autor, downloads e link `modrinth.com/project/<slug>`.
- Sem resultados, responde "Nenhum mod encontrado para '<texto>'".
- Documentação da API: <https://docs.modrinth.com/api/>.

> [!warning] Observações
> - O arquivo se chama `buscar_mod.py`, mas o comando é **`/busca_mod`**.
> - `requests.get` é bloqueante e não tem `timeout`: enquanto espera o Modrinth, o bot não atende mais ninguém. O Modrinth pede um `User-Agent` que identifique o projeto.
> - Erros HTTP e JSON inválido não são tratados.
