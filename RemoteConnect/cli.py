# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_cli.ipynb (unless otherwise specified).

__all__ = ['start_code', 'start_jupyter', 'start_pluto']

# Cell
from fastcore.script import call_parse, Param, bool_arg
from .core import RemoteCode, RemoteJupyter, RemotePluto, IN_COLAB, mount_drive

# Cell
@call_parse
def start_code(port:Param("Port to Start Code", type=int)=10000,
               password:Param("Password to Start Code", type=str)=None,
               tunnel:Param("Tunel Type", type=str)='ngrok',
               authtoken:Param("Tunnel Authtoken for ngrok", type=str)=None):
    "Starts Code Server"
    if IN_COLAB: mount_drive()
    RemoteCode(password=password, port=port, tunnel=tunnel, authtoken=authtoken)


# Cell
@call_parse
def start_jupyter(port:Param("Port to Start Jupyter", type=int)=9000,
                  ui:Param("Interface to start", type=str)='notebook',
                  tunnel:Param("Tunel Type", type=str)='ngrok',
                  authtoken:Param("Tunnel Authtoken for ngrok", type=str)=None):
    "Starts Jupyter"
    if IN_COLAB: mount_drive()
    RemoteJupyter(port=port, ui=ui, tunnel=tunnel, authtoken=authtoken)

# Cell
@call_parse
def start_pluto(port:Param("Port to Start Jupyter", type=int)=9000,
                tunnel:Param("Tunel Type", type=str)='ngrok',
                authtoken:Param("Tunnel Authtoken for ngrok", type=str)=None):
    "Starts Pluto.jl reactive notebook"
    if IN_COLAB: mount_drive()
    RemotePluto(port=port, tunnel=tunnel, authtoken=authtoken)