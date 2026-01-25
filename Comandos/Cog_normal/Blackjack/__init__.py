from .blackjack_group import blackjack_group
import pkgutil, importlib

package_name = __name__
for finder, name, ispkg in pkgutil.iter_modules(__path__):
    if name == "blackjack_group":
        continue
    importlib.import_module(f"{package_name}.{name}")

__all__ = ("blackjack_group",)
