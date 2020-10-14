# windows-wsl-sandbox

### Scope

With this reusable Playbook it should install common libs automatically in a Windows-WSL environment.

### Requirement

* WSL2 environment
* ansible version: 2.9.6 (you can install it by using python-pip3)

### install deep learning libs

The installation contains the newest version of tensorflow and pytorch.

* tensorflow 2.1
* tensorboard
* pytorch 1.4 
* torchvision
* jupyter

Jupyter can provide a https user web interface by starting jupyter server. You can access this development environment via https://< your ecs public ip >:8888

### HandsOn - Setup WSL Env

### Setup your wsl env with ansible-playbook
The requirements.txt file contains ansible dependency, which means you can use command-line-tool ansible-playbook directly...

1. Checking if host is accessible

```
$ ansible all -m ping
```
2. Install deep learning libraries (need to provide password here)
```
$ ansible-playbook -c local -i localhost, setup-wsl-instance.yml  --ask-become-pass
```

### Start jupyter notebook
Once your ansible-playbook is finished, you should do following steps to start jupyter server:

Login with ssh

```
$ ssh wsl@(your ip)

# set password for jupyter remote login
$ jupyter notebook password
  Enter password:  ****
  Verify password: ****
  
# my ansible playbook has generated cert.pem and key.key for secured access
$ wsl@iZgw89wtwllnq3g945jw7iZ:~/.jupyter$ jupyter notebook --certfile=mycert.pem --keyfile mykey.key
```

### Extra Delete User and ansible generated files
TBD