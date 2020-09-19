# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_cli.ipynb (unless otherwise specified).

__all__ = ['start_code', 'start_jupyter']

# Cell
from fastscript import call_parse, Param, bool_arg
from .core import RemoteCode, RemoteJupyter, IN_COLAB, mount_drive

# Cell
@call_parse
def start_code(port:Param("Port to Start Code", type=int)=10000,
               password:Param("Password to Start Code", type=str)=None):
    "Starts Code Server"
    if IN_COLAB:
        mount_drive()
    print(RemoteCode(password=password, port=port))


# Cell
@call_parse
def start_jupyter(port:Param("Port to Start Code", type=int)=9000):
    "Starts Jupyter"
    if IN_COLAB:
        mount_drive()
    RemoteJupyter(port=port)