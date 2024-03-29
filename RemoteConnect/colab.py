# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_colab.ipynb (unless otherwise specified).

__all__ = ['setup_gh', 'RemoteProject']

# Cell
from fastcore.basics import in_colab, in_jupyter
from .core import  mount_drive, execute_cmd
import configparser
import os
import pathlib
import subprocess

# Cell
def setup_gh():
    print(f"Inside directory : {get_ipython().magic('pwd')}")
    if not os.path.exists("install_gh.sh"):
        execute_cmd("wget https://gist.githubusercontent.com/Rahuketu86/ee87106a40b37403f20e115fca2fb7c1/raw/f146adc691cf9a64f5c916dcebac5c09b8e0741f/install_gh.sh")
    execute_cmd("bash install_gh.sh")

# Cell
class RemoteProject(object):
    def __init__(self, cfg_path, cfg_name, is_nbdev=True):
        if in_colab(): mount_drive()
        self.is_nbdev = is_nbdev
        self.cfg_path = cfg_path
        self.cfg_name = cfg_name
        self.cfg = configparser.ConfigParser()
        self.cfg.read_file((pathlib.Path(self.cfg_path)/self.cfg_name).open('r'))
        self.git_pat = pathlib.Path(self.cfg['DEFAULT']['git_user_pat']).read_text()
        self.git_username = self.cfg['DEFAULT']['git_user_name']
        self.git_useremail = self.cfg['DEFAULT']['git_user_email']
        self.setup_git_global()

    @property
    def projects(self):
        return self.cfg.sections()


    def git_auth_url(self, proj_name):
        git_url = self.cfg[proj_name]['git_url']
        url = f"https://{self.git_username}:{self.git_pat}@github.com/{git_url}.git"
        return url

    def get_project(self, proj_name):
        root = pathlib.Path(self.cfg['DEFAULT']['project_path'])
        project_loc = root/proj_name
        if project_loc.exists():
            if in_colab() or in_jupyter():self.setup_project_env(project_loc)
        else:
            if in_colab() or in_jupyter():
                self.clone_setup_repo(proj_name)
                self.setup_project_env(project_loc)
        return project_loc

    def setup_git_global(self):
        if in_colab():
            root = pathlib.Path(self.cfg['DEFAULT']['project_path'])
            get_ipython().magic(f"cd {root}")
            setup_gh()
        execute_cmd(f"git config --global user.name  {self.git_username}")
        execute_cmd(f"git config --global user.email {self.git_useremail}")
        execute_cmd(f"git config credential.helper store")
        execute_cmd(f"gh auth login --with-token < {self.cfg['DEFAULT']['git_user_pat']}")
        execute_cmd(f'gh auth status')
        # execute_cmd()


    def setup_project_env(self, project_loc):
        get_ipython().magic(f"cd {project_loc}")
        if self.is_nbdev:
            execute_cmd(f"nbdev_install_git_hooks")
            print("Installing local package")
            execute_cmd(f"pip3 install -e .[dev]")
            execute_cmd("bash update_colab.sh")

    def clone_setup_repo(self, proj_name):
        execute_cmd(f"gh auth login --with-token {self.cfg['DEFAULT']['git_user_pat']}")
        root = pathlib.Path(self.cfg['DEFAULT']['project_path'])
        get_ipython().magic(f"cd {root}")
        project_loc = root/proj_name
        execute_cmd(cmd = f"git clone {self.git_auth_url(proj_name)}", show_cmd="Cloning Repo")

    def save(self):
        return self.cfg.write((pathlib.Path(self.cfg_path)/self.cfg_name).open('w'))

    def add_project(self, proj_name, git_url, git_branch, force=True):
        if proj_name in self.projects and force:
            self.cfg.remove_section(proj_name)
        self.cfg.add_section(proj_name)
        self.cfg[proj_name]['git_url'] = git_url
        self.cfg[proj_name]['git_branch'] = git_branch
        self.save()