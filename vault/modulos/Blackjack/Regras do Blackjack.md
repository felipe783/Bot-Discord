# Sobre os Arquivos

`iniciar.py`, `hit.py`, `stand.py`, `double_down.py` e `Estados/estados_Blackjack.py` implementam o **Blackjack contra o dealer**, em que a aposta é o **tempo de *timeout*** de quem perde.

Pasta: `Comandos/Cog_normal/Groups/Blackjack/` (command group `/blackjack`); estado das mesas em `Estados/estados_Blackjack.py`.
# Funcionalidades

## Estado

````python
jogos = {}   # user_id -> mesa
estados_Blackjack.jogos[user_id] = {
    "baralho": baralho, "mao": mao_user, "dealer": mao_dealer,
    "aposta": aposta, "doubledown": True, "stand": True,
    "pontos": 0, "pontos_dealer": 0,
}
````

Uma mesa por usuário, **em memória**: reiniciar o bot encerra todas as partidas.

## Pontuação

````python
def calcular_pontos(mao):
    total = sum(c["valor"] for c in mao)       # Ás = 11, figuras = 10
    ases = sum(1 for c in mao if c["nome"] == "Ás")
    while total > 21 and ases:
        total -= 10; ases -= 1                  # Ás vira 1 enquanto estourar
    return total
````

Baralho único de 52 cartas, embaralhado com `random.shuffle` a cada partida.

## Subcomandos

| Comando | Regra implementada |
|---|---|
| `iniciar <aposta>` | `aposta > 0`; 2 cartas para cada um. Blackjack natural: empate se ambos, vitória do jogador, ou derrota com *timeout* se só o dealer |
| `hit` | o jogador compra 1 carta **e o dealer também**; o dealer então compra até 17. Jogador > 21 → derrota com *timeout*; dealer > 21 → partida encerrada; senão continua. Desativa o `double_down` |
| `stand` | dealer compra até 17 e os pontos são comparados; derrota → *timeout* de `aposta` minutos |
| `double_down` | só antes de qualquer `hit`; dobra a aposta, jogador **e dealer** compram 1 carta cada (o dealer **não** compra até 17) e a partida é resolvida na hora |

> [!warning] Observações
> - No `hit`, o dealer recebe uma carta a cada compra do jogador, o que não é a regra do Blackjack tradicional.
> - Empate só é tratado quando os dois fazem exatamente 21; com outra pontuação igual, o dealer vence.
> - `interaction.user.timeout(...)` exige a permissão *Moderate Members* e falha em administradores e no dono do servidor (`Forbidden`, sem tratamento).
> - `aposta` não tem limite superior: o Discord aceita no máximo 28 dias de *timeout*.
> - `formatar_mao` e `calcular_pontos` estão copiadas nos 4 arquivos.
