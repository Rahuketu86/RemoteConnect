# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb (unless otherwise specified).

__all__ = ['IN_COLAB', 'EXTENSIONS', 'say_hello', 'connect_to_ngrok', 'execute_cmd', 'mount_drive', 'setup_vscode',
           'setup_julia', 'RemoteCode', 'NOTEBOOK_EXTENSIONS', 'SERVER_EXTENSIONS', 'LAB_EXTENSIONS', 'RemoteJupyter',
           'RemotePluto']

# Cell
# IN_COLAB = 'google.colab' in str(get_ipython())
# if IN_COLAB:
#     from google.colab import drive

IN_COLAB = False
try:
    from google.colab import drive

    IN_COLAB = True
except ImportError:
    IN_COLAB = False
import os
import subprocess
from pyngrok import ngrok

# Cell
EXTENSIONS = ["ms-python.python", "jithurjacob.nbpreviewer"]

# Cell
def say_hello(to):
    print(f"Say hello to {to}")

# Cell
def connect_to_ngrok(port):
    active_tunnels = ngrok.get_tunnels()
    for tunnel in active_tunnels:
        public_url = tunnel.public_url
        print(f"Disconnecting {public_url}")
        ngrok.disconnect(public_url)
    url = ngrok.connect(port=port, options={"bind_tls":True})
    print(f"Remote server can be assesed on : {url}")
    return url

# Cell
def execute_cmd(cmd):
    print(f"Executing >>> {cmd}")
    with subprocess.Popen(
        [cmd],
        shell=True,
        stdout=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
    ) as proc:
        for line in proc.stdout:
            print(line, end="")

# Cell
def mount_drive():
    drive.mount("/content/drive")

# Cell
def setup_vscode():
    subprocess.run(
            ["wget", "https://code-server.dev/install.sh"], stdout=subprocess.PIPE
        )
    subprocess.run(["sh", "install.sh"], stdout=subprocess.PIPE)
    for ext in EXTENSIONS:
        subprocess.run(["code-server", "--install-extension", f"{ext}"])


# Cell
def setup_julia():
    subprocess.run(
            ["wget", "https://gist.githubusercontent.com/Rahuketu86/3543336b8fe4ea2c1cc7b6edcc96f975/raw/db6c562201ecf655b0bb82d7fcd2a16128bb0148/install_julia.sh"], stdout=subprocess.PIPE
        )
    execute_cmd("bash install_julia.sh")

# Cell
class RemoteCode:
    """ Install and launch an instance of Remote Code"""
    def __init__(self, port=10000, password=None):
        self.port = port
        self.password = password
        self._mount = IN_COLAB
        self.url = None
        self._install_code()
        self._install_extensions()
        self._start_server()
        self._run_code()

    def _install_code(self):
        subprocess.run(
            ["wget", "https://code-server.dev/install.sh"], stdout=subprocess.PIPE
        )
        subprocess.run(["sh", "install.sh"], stdout=subprocess.PIPE)

    def _install_extensions(self):
        for ext in EXTENSIONS:
            subprocess.run(["code-server", "--install-extension", f"{ext}"])

    def _start_server(self):
        self.url = connect_to_ngrok(self.port)

    def _run_code(self):
        os.system(f"fuser -n tcp -k {self.port}")
#         if IN_COLAB:
#             drive.mount("/content/drive")
        if self.password:
            code_cmd = f"PASSWORD={self.password} code-server --port {self.port} --disable-telemetry"
        else:
            code_cmd = f"code-server --port {self.port} --auth none --disable-telemetry"
        execute_cmd(code_cmd)

    def __str__(self):
        return f"Remote Code runnning on {self.url}:{self.port} with password:{self.password} in colab envrionment:{IN_COLAB}"


# Cell
NOTEBOOK_EXTENSIONS = ["toc2/main", "collapsible_headings/main", "execute_time/ExecuteTime", "codefolding/main"]

SERVER_EXTENSIONS=["jupyter_server_proxy"]
LAB_EXTENSIONS=["@jupyterlab/server-proxy"]

# Cell
class RemoteJupyter:
    """ Install and launch an instance of Remote Jupyter"""
    def __init__(self, port=9000, ui='notebook'):
        self.port = port
        self._mount = IN_COLAB
        self.url = None
        self.ui = ui
        if IN_COLAB:
            self._install_extensions()
        self._start_server()
        self._run_jupyter()

    def _install_extensions(self):
        subprocess.run(["jupyter", "contrib", "nbextension","install",  "--system"], stdout=subprocess.PIPE)
        #nbextensions_configurator enable --user
        subprocess.run(["jupyter", "nbextensions_configurator","enable",  "--system"], stdout=subprocess.PIPE)
        for ext in NOTEBOOK_EXTENSIONS:
            subprocess.run(["jupyter", "nbextension", "enable", ext], stdout=subprocess.PIPE)
        for ext in SERVER_EXTENSIONS:
            subprocess.run(["jupyter", "serverextension", "enable", ext], stdout=subprocess.PIPE)

        for ext in LAB_EXTENSIONS:
            subprocess.run(["jupyter", "labextension", "enable", ext], stdout=subprocess.PIPE)

    def _start_server(self):
        self.url = connect_to_ngrok(self.port)

    def _run_jupyter(self):
        os.system(f"fuser -n tcp -k {self.port}")
        print(self.url)
#         if IN_COLAB:
#             drive.mount("/content/drive")
        jupyter_cmd = f"jupyter {self.ui} --NotebookApp.allow_remote_access=True  --NotebookApp.disable_check_xsrf=True --ip=0.0.0.0 --port={self.port}"
        if self.ui == 'lab':
            jupyter_cmd = f"jupyter {self.ui} --ip=0.0.0.0 --port={self.port} --no-browser"
        execute_cmd(jupyter_cmd)

    def __str__(self):
        return f"Remote Jupyter runnning on {self.url}:{self.port} with password:{self.password} in colab envrionment:{IN_COLAB}"

# Cell
class RemotePluto:
    """ Install and launch an instance of Remote Pluto.jl for Julia⌈"""
    def __init__(self, port=9000):
        self.port = port
        self._mount = IN_COLAB
        setup_julia()
        self._start_server()
        self._run_pluto()


    def _start_server(self):
        self.url = connect_to_ngrok(self.port)

    def _run_pluto(self):
        os.system(f"fuser -n tcp -k {self.port}")
        print(self.url)
#         if IN_COLAB:
#             drive.mount("/content/drive")
        pluto_cmd = f'julia -e "using Pluto;Pluto.run(port={self.port}, launch_browser=false, require_secret_for_open_links=false, require_secret_for_access=false)"'
#         if self.ui == 'lab':
#             jupyter_cmd = f"jupyter {self.ui} --ip=0.0.0.0 --port={self.port} --no-browser"
        execute_cmd(pluto_cmd)

    def __str__(self):
        return f"Remote Pluto runnning on {self.url}:{self.port} with password:{self.password} in colab envrionment:{IN_COLAB}"