# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb (unless otherwise specified).

__all__ = ['say_hello', 'IN_COLAB', 'connect_to_telebit', 'connect_to_localtunel', 'connect_to_ngrok', 'execute_cmd',
           'mount_drive', 'setup_vscode', 'setup_julia', 'RemoteExecutor', 'EXTENSIONS', 'RemoteCode',
           'NOTEBOOK_EXTENSIONS', 'SERVER_EXTENSIONS', 'LAB_EXTENSIONS', 'RemoteJupyter', 'RemotePluto']

# Cell
import os
import subprocess
import re
import time
from pyngrok import ngrok
from fastcore.meta import delegates
from IPython import get_ipython
import pathlib

# Cell
def say_hello(to):
    print(f"Say hello to {to}")

# Cell
IN_COLAB = 'google.colab' in str(get_ipython())

# Cell
def connect_to_telebit(port):
    try:
        s = subprocess.check_output(f"~/telebit http {port}", stderr=subprocess.STDOUT, shell=True)
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(s))[0]
        print(f"Remote server can be assesed on : {url}")
        return url
    except CalledProcessError:
        print("Need to install and register device with telebit first")

# Cell
def connect_to_localtunel(port):
    try:
        url_folder = pathlib.Path.home()
        if IN_COLAB:
            url_folder = pathlib.Path.cwd()
            print("Installing localtunnel on colab")
            subprocess.run("npm install -g localtunnel")
            time.sleep(1)
            print("Finished Installation")
        subprocess.run(f"lt --port {port} --subdomain nbrahuketu>> ~/url.txt 2>&1 &", stderr=subprocess.STDOUT, shell=True)
        time.sleep(1)
        s = pathlib.Path(f"{url_folder}/url.txt").open().read()
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(s))[-1]
        print(f"Remote server can be assesed on : {url}")
        return url
    except CalledProcessError:
        print("Need to install localtunnel first")

# Cell
def connect_to_ngrok(port, authtoken=None):
    time.sleep(1)
    try:
        active_tunnels = ngrok.get_tunnels()
        time.sleep(1)
        for tunnel in active_tunnels:
            public_url = tunnel.public_url
            print(f"Disconnecting {public_url}")
            ngrok.disconnect(public_url)
            time.sleep(1)
    except:
        print("Some error in ngrok.get_tunnels()")
#     url = ngrok.connect(addr=port, options={"bind_tls":True})
    if authtoken:ngrok.set_auth_token(authtoken)
    url = ngrok.connect(addr=port, bind_tls=True)
    time.sleep(1)
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
    from google.colab import drive
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
    if IN_COLAB:
        subprocess.run(
                ["wget", "https://gist.githubusercontent.com/Rahuketu86/765ee2ecd59aa40c493fe6a10db606a4/raw/a3498236fb96109e0f6ed2ea8325cf8acafe75d0/install_julia_colab.sh"], stdout=subprocess.PIPE
            )
        execute_cmd("bash install_julia_colab.sh")
    else:
        subprocess.run(
                ["wget", "https://gist.githubusercontent.com/Rahuketu86/3543336b8fe4ea2c1cc7b6edcc96f975/raw/db6c562201ecf655b0bb82d7fcd2a16128bb0148/install_julia.sh"], stdout=subprocess.PIPE
            )
        execute_cmd("bash install_julia.sh")

# Cell
class RemoteExecutor(object):
    def __init__(self, port=9000, tunnel='ngrok', authtoken=None, password=None, ui='notebook',
                 install_code=False, install_julia=False):
        self.port = port
        self.tunnel = tunnel
        self.authtoken = authtoken
        self.password = password
        self.ui = ui
        self.url = None
        self.install_code = install_code
        self.install_julia = install_julia

    def launch(self):
        self.install()
        if IN_COLAB:self.preinstall_colab()
        self.start_server()
        self.run()

    def preinstall_colab(self):
        if self.install_code : setup_vscode()
        if self.install_julia : setup_julia()
        self.install_extensions()

    def install(self):
        pass

    def install_extensions(self):
        pass

    def start_server(self):
        if self.tunnel == 'ngrok':
            self.url = connect_to_ngrok(self.port, self.authtoken)
        elif self.tunnel == 'telebit':
            self.url = connect_to_telebit(self.port)
        elif self.tunnel == 'localtunnel':
            self.url = connect_to_localtunel(self.port)
        else:
            raise Exception("Tunnel not specified")

    def run(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__} runnning on {self.url}:{self.port}  in colab envrionment:{IN_COLAB}"


# Cell
EXTENSIONS = ["ms-python.python", "jithurjacob.nbpreviewer"]

# Cell
@delegates()
class RemoteCode(RemoteExecutor):
    """ Install and launch an instance of Remote Code"""

    def __init__(self, password=None, **kwargs):
        super(RemoteCode, self).__init__(**kwargs)
        self.password = password

    def preinstall_colab(self):
        setup_vscode()
        self.install_extensions()

    def install_extensions(self):
        for ext in EXTENSIONS:
            subprocess.run(["code-server", "--install-extension", f"{ext}"])

    def run(self):
        os.system(f"fuser -n tcp -k {self.port}")
        if self.password:
            code_cmd = f"PASSWORD={self.password} code-server --port {self.port} --disable-telemetry"
        else:
            code_cmd = f"code-server --port {self.port} --auth none --disable-telemetry"
        execute_cmd(code_cmd)

# Cell
NOTEBOOK_EXTENSIONS = ["toc2/main", "collapsible_headings/main", "execute_time/ExecuteTime", "codefolding/main"]
SERVER_EXTENSIONS=["jupyter_server_proxy"]
LAB_EXTENSIONS=["@jupyterlab/server-proxy"]

# Cell
@delegates()
class RemoteJupyter(RemoteExecutor):
    """ Install and launch an instance of Remote Jupyter"""

    def __init__(self, ui='notebook', **kwargs):
        super(RemoteJupyter, self).__init__(**kwargs)
        self.ui = ui

    def install_extension(self):
        subprocess.run(["jupyter", "contrib", "nbextension","install",  "--system"], stdout=subprocess.PIPE)
        #nbextensions_configurator enable --user
        subprocess.run(["jupyter", "nbextensions_configurator","enable",  "--system"], stdout=subprocess.PIPE)
        for ext in NOTEBOOK_EXTENSIONS:
            subprocess.run(["jupyter", "nbextension", "enable", ext], stdout=subprocess.PIPE)

        for ext in SERVER_EXTENSIONS:
            subprocess.run(["jupyter", "serverextension", "enable", ext], stdout=subprocess.PIPE)

        for ext in LAB_EXTENSIONS:
            subprocess.run(["jupyter", "labextension", "enable", ext], stdout=subprocess.PIPE)

    def run(self):
        os.system(f"fuser -n tcp -k {self.port}")
        jupyter_cmd = f"jupyter {self.ui} --NotebookApp.allow_remote_access=True  --NotebookApp.disable_check_xsrf=True --ip=0.0.0.0 --port={self.port}"
        if self.ui == 'lab':
            jupyter_cmd = f"jupyter {self.ui} --ip=0.0.0.0 --port={self.port} --no-browser"
        execute_cmd(jupyter_cmd)

# Cell
@delegates()
class RemotePluto(RemoteExecutor):
    """ Install and launch an instance of Remote Pluto.jl for Julia"""

    def __init__(self, **kwargs):
        super(RemotePluto, self).__init__(**kwargs)

    def preinstall_colab(self):
        setup_julia()
        self.install_extensions()

    def run(self):
        os.system(f"fuser -n tcp -k {self.port}")
        print(self.url)
        pluto_cmd = f'julia -e "using Pluto;Pluto.run(port={self.port}, launch_browser=false, require_secret_for_open_links=false, require_secret_for_access=false)"'
        execute_cmd(pluto_cmd)