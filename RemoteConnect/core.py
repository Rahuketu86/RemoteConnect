# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb (unless otherwise specified).

__all__ = ['IN_COLAB', 'EXTENSIONS', 'say_hello', 'connect_to_ngrok', 'RemoteCode', 'NOTEBOOK_EXTENSIONS',
           'RemoteJupyter']

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
        if IN_COLAB:
            drive.mount("/content/drive")
        if self.password:
            code_cmd = f"PASSWORD={self.password} code-server --port {self.port} --disable-telemetry"
        else:
            code_cmd = f"code-server --port {self.port} --auth none --disable-telemetry"
        with subprocess.Popen(
            [code_cmd],
            shell=True,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            for line in proc.stdout:
                print(line, end="")

    def __str__(self):
        return f"Remote Code runnning on {self.url}:{self.port} with password:{self.password} in colab envrionment:{IN_COLAB}"


# Cell
NOTEBOOK_EXTENSIONS = ["toc2", "collapsible_headings"]

# Cell
class RemoteJupyter:
    """ Install and launch an instance of Remote Jupyter"""
    def __init__(self, port=9000):
        self.port = port
        self._mount = IN_COLAB
        self.url = None
        if IN_COLAB:
            self._install_extensions()
        self._start_server()
        self._run_jupyter()


    def _install_extensions(self):
        subprocess.run(["jupyter", "contrib", "nbextension","install",  "--system"], stdout=subprocess.PIPE)
        #nbextensions_configurator enable --user
        subprocess.run(["jupyter", "nbextensions_configurator","enable",  "--system"], stdout=subprocess.PIPE)
        for ext in NOTEBOOK_EXTENSIONS:
            subprocess.run([f"jupyter nbextension enable {ext}/main"], stdout=subprocess.PIPE)

    def _start_server(self):
        self.url = connect_to_ngrok(self.port)

    def _run_jupyter(self):
        os.system(f"fuser -n tcp -k {self.port}")
        print(self.url)
        if IN_COLAB:
            drive.mount("/content/drive")
        jupyter_cmd = f"jupyter notebook --NotebookApp.allow_remote_access=True --ip=0.0.0.0 --port={self.port}"
        with subprocess.Popen(
            [jupyter_cmd],
            shell=True,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            for line in proc.stdout:
                print(line, end="")