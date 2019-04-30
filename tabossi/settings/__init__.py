
try:
    from .local import *
except ImportError:
    print("local.py not found")
    from .dev import *
