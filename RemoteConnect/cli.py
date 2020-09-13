# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_cli.ipynb (unless otherwise specified).

__all__ = ['start_code']

# Cell
from nbdev.showdoc import *
from fastscript import call_parse, Param, bool_arg
from .core import *

# Cell
@call_parse
def start_code(port:Param("Port to Start Code", type=int)=10000):
    "Start Code Server"
    print(f"Starting Code-Lib {port}")
