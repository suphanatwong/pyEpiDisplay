import pkgutil
import importlib

__all__ = []

for module_info in pkgutil.iter_modules(__path__):
    module_name = module_info.name
    globals()[module_name] = importlib.import_module(f"{__name__}.{module_name}")
    __all__.append(module_name)
