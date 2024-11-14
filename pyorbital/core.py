"""Fill in a module description here"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['say_hello', 'HelloSayer']

# %% ../nbs/00_core.ipynb 3
def say_hello(to):
    "Say hello to somebody"
    return f'Hello {to}!'

# %% ../nbs/00_core.ipynb 5
class HelloSayer:
    "Say hello to `to` using `say_hello`"
    def __init__(self, to): self.to = to
        
    def say(self):
        "Do the saying"
        return say_hello(self.to)
