import pkgutil
import importlib

__all__ = []

for module_info in pkgutil.iter_modules(__path__):
    module_name = module_info.name
    module = importlib.import_module(f"{__name__}.{module_name}")

    # get names to export
    if hasattr(module, "__all__"):
        names = module.__all__
    else:
        # export only callables (functions/classes), ignore modules
        names = [
            n for n in dir(module)
            if not n.startswith("_")
            and callable(getattr(module, n))
        ]

    for name in names:
        globals()[name] = getattr(module, name)

    __all__.extend(names)
