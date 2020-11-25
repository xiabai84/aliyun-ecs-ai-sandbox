# windows-wsl-sandbox

### Scope

With this reusable playbook it should install common libs automatically on your local windows-wsl environment.

There is still some hardcode in the scripts...TBD

### Requirement

* WSL2 environment
* root password (playbook will run as a root user)
* ansible version: 2.9.6 (you can install it by using python-pip3)

If you don't have python3 and pip installed on your wsl ubuntu system yet:

```
$ sudo apt-get install python3.6
$ sudo apt install python3-pip
```

Configure .bashrc env variables

```
alias python=python3
alias pip=pip3
export ANSIBLE_HOME='/home/xiabai84/.local'
export PATH=$PATH:$ANSIBLE_HOME/bin
```

Install ansible

```
$ pip install ansible==2.9.6
```

now you are ready to run ansible playbook


### playbook settings

Setting ownership of installation by using vars in setup-wsl-instance.yml file.

```
- hosts: "localhost"
  vars:
    wsl_user: xiabai84
```

This means, that all installation related packages and files belong to wsl-default-user "xiabai84" in my case. This is a important setting in WSL env, because only this user has certain privilege for interacting with windows host system. If use other linux user instead default-user, it could have problems with opening or creating tmp-files...

### install docker-ce

### install openjdk-11

### install deep learning libs

The installation contains the newest version of tensorflow and pytorch.

* tensorflow 2.1
* tensorboard
* pytorch 1.4 
* torchvision
* jupyter

Jupyter can provide a https user web interface by starting jupyter server. You can access this development environment via https://localhost:8888

### HandsOn - Setup WSL Env

### Setup your wsl env with ansible-playbook
The requirements.txt file contains ansible dependency, which means you can use command-line-tool ansible-playbook directly...

1. Checking if host is accessible

```
$ ansible all -m ping
```
2. Begin installation (need to provide password here)
```
$ ansible-playbook -c local -i localhost, setup-wsl-instance.yml --ask-become-pass
```

### Start jupyter notebook
Once your ansible-playbook is finished, you should do following steps to start jupyter server:

Login with ssh

```
$ su wsl

# set password for jupyter remote login
$ jupyter notebook password
  Enter password:  ****
  Verify password: ****
  
# my ansible playbook has generated cert.pem and key.key for secured access
$ wsl@DESKTOP-LUMRQMO:~/.jupyter$ jupyter notebook --certfile=mycert.pem --keyfile mykey.key
```

### Extra Delete User and ansible generated files
Delete user wsl (need to provide password here). 

It will also clean the following directories...
```
/mnt/data
/mnt/wsl
/home/wsl
```

```
$ ansible-playbook -c local -i localhost, delete_wsl_user.yml --ask-become-pass
```
