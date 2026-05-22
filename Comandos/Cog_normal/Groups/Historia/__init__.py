from .historia_group import historia_group
import pkgutil, importlib

package_name = __name__
for finder, name, ispkg in pkgutil.iter_modules(__path__):
    if name == "historia_group":
        continue
    importlib.import_module(f"{package_name}.{name}")

async def setup(bot):
    pass

__all__ = ("historia_group",)
