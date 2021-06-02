# Remote Connect
> Launch Code , Jupyter or other apps from colab and OEC


## Install

- For development (editable version)
  
  ```pip install -e .```
  
- For latest version 

   ```!pip install -U git+https://github.com/Rahuketu86/RemoteConnect.git```

## How to use

- Open a colab notebook
    - Install the RemoteConnect package if on colab

      ```!pip install -U git+https://github.com/Rahuketu86/RemoteConnect.git```

    - For running VSCode on Remote Machine ( Server or Colab)

      ```!start_code --port=<port> --password=<password> --tunnel=<str:ngrok|telebit>```

    - For running Jupyter on Remote Machine ( Server or Colab)

      ```!start_jupyter --port=<port>  --ui=<str:lab|notebook> --tunnel=<str:ngrok|telebit>```
      
      Default ui options is notebook. To open lab interface pass `--ui lab`

    - For running Pluto.jl reactive notebook(Only Server)

      ```!start_pluto --port=<port> --tunnel=<str:ngrok|telebit>```
  
- On Remote Server
    - It might be beneficial to register ngrok authtoken <token> after installation 

##  ProxyServers

- Added Code and Pluto as jupyter server proxy
    - Accessible at `Pluto.jl` in notebook or `/pluto` on url
    - Accessible at `Vscodium` in notebook or `/codium` on url
- Added docserver and bookserver for nbdev and jupyterbook
    - Accessible at `docserver` in notebook or `/docserver` on url
    - Accessible at `bookserver` in notebook or `/bookserver` on url
