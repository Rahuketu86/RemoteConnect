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

      ```!start_code --port=<port> --password=<password>```

    - For running Jupyter on Remote Machine ( Server or Colab)

      ```!start_jupyter --port=<port>```
  
  
- On Remote Server
    - It might be beneficial to register ngrok authtoken <token> after installation 
