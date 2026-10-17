# Sobre os Arquivos

`loader.py` e `Json/Data.json` formam a **Persistência do Bot**.
# Funcionalidades

````python
def load_db():
    if os.path.exists("Json/Data.json"):
        with open("Json/Data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_db(dados):
    with open("Json/Data.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
````

## Formato do Data.json

| Chave | Tipo | Uso |
|---|---|---|
| `historia` | `list[str]` | frases da história atual |
| `ID_Historia` | `list[int]` | ID do canal `historias` (só o primeiro é usado) |
| `mod` | `dict` | `id, slug, title, description, downloads, icon_url` (não é lido pelo código atual) |

> [!warning] Observações
> - Sem o arquivo, `load_db()` devolve `[]` (lista), mas o resto do código espera um `dict`.
> - O caminho é relativo ao diretório atual: rode o bot da raiz.
> - O arquivo é **versionado no Git** e gravado sem trava. No Docker, fica dentro do container, sem volume.
> - Vários módulos chamam `load_db()` na importação e guardam o resultado em `DB`, que não acompanha mudanças posteriores no arquivo.
