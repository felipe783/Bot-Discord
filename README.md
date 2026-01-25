# Bot Teste🔥

## Comandos Normais:
> ***Comandos onde qualquer um pode usar***

### /ajuda
- Neste comando ira mostrar a `lista de comandos` do bot e uma pequena explicação sobre eles

### /ping
- O bot vai `responder` quem chamou com um `pong`

### /historia {texto}
> O argumento texto é obrigátorio

- Neste comando sera possivel `juntar` as `frases(texto)` escritas pelos membros do servidor e formar uma `historia`
- E a cada dia as `historias` são zeradas e é enviado uma `copia` inteira da `ultima historia` no `canal historia`

### /ver historia

- Neste comando é possivel ver como esta a `historia`

### /blackjack 
- É um **group command**
    #### /blackjack iniciar {aposta}
    > O argumento **Aposta** é obrigátorio
    - Inicia um jogo de `BlackJack`

    #### /blackjack double_down
    - Dobra a `aposta`,compra mais uma `carta`
    - E entra em stand automatico 
    
    #### /blackjack stand
    - `Para de comprar cartas` e ve se tem a maior pontuação sem estourar

    #### /blackjack hit
    - O jogador compra `mais uma carta` 
    - Pode `repetir` o `quanto quiser`,desde que `não estoure`

### /buscar_mod
>[Documentação da API](https://docs.modrinth.com/api/)
- Comando onde usa a API `Labrinth` criada pela equipe do `Modrinth`
- Neste comando o usuário escreve o nome de um `mod` e a API faz a busca e forneece as informações:`descrição,donwloads,autor`

## Comandos ADM:
> ***São comandos onde apenas pessoas com determinado cargo podem usar***,que no caso é o cargo `ADM`

### /apagar

- Neste comando é possivel apagar a historia antes do tempo de reset delas *(24 horas)*

### /reload

- Neste comando é possivel dar `Reload` em todos os comandos

## Cogs de Criar canais:

- Nesta pasta são criados os canais onde o bot ira necessitar para funcionar corretamento como o `canal História`
