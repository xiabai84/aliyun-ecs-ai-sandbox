# aliyun-ecs-ai-sandbox

This is a automation script for building machine learning dev-environment on Alibaba Cloud, which is hosted in german region (Frankfurt am Main) by default setting.<br>

In thi project I use Alibaba Cloud python sdk for creating ECS instance (actually Terraform can do the same thing). There is also a ansible-playbook for installing nvidia drivers and deep learning libs with GPU support. This guide assumes that you use Ubuntu 18.04, the playbook may need some editing if you're using other versions of ubuntu or linux... 

### Deep Learning libraries

The installation contains the newest version of tensorflow and pytorch.

* tensorflow 2.1
* tensorboard
* pytorch 1.4 
* torchvision
* jupyter
* cuda 10.2

Jupyter can provide a https user web interface by starting jupyter server. You can access this development environment via https://< your ecs public ip >:8888

### HandsOn - Setup EMS instance
1 Install python3 dependencies

Assume you already have python3 and virtualenvwrapper on your local machine (https://virtualenvwrapper.readthedocs.io/en/latest/)

```
$ mkvirtualenv ali-cloud
$ workon ali-cloud
$ pip install -r requirements.txt
```
2 Setup basic configurations in Alibaba Cloud

For remote access, you must generate ACCESS_KEY_ID and ACCESS_KEY_SECRET for your account. 
See: https://www.alibabacloud.com/help/doc-detail/142101.htm

3 Create ECS instance

Start init python script and follow hints to create ECS instance:

```
$ python setup_ecs_instance.py
```
* Enter ACCESS_KEY_ID and ACCESS_KEY_SECRET. You can find them unter Alibaba Cloud -> User Management -> Security Management

* Choose region, where this instance should be hosted -> **eu-central-1** is the EU data center, which is hosted in Frankfurt

* Choose a instance type(hardware requirement). There are lots of available instance types. Because we always want to achieve big AI workload in the cloud with GPU, therefore I contraint them to only list GPU instances.
For example **ecs.gn5-c4g1.xlarge** has **NVIDIA P100** GPU. For more information about this type of instance you can find them in Alibaba Home Page

* Then select disks and zone settings... Just use my predefined default settings, if you don't really familiar with such cloud configurations.

* For SecurityGroup I use a basic network configurations such as common http/https, ssh and jupyter server web ui (port 8888)

* SSH KeyValue -> You need to generate your own id_rsa, id_rsa.pub and use id_rsa.pub for cloud setting. These ssh-keys enable you can access your ECS instance from Unix console. For more information see https://www.alibabacloud.com/help/doc-detail/51793.html

* Choose Base-Image for OS, all of installtion in the next steps are based on ubuntu_18_04_x64_20G_alibase_20200220.vhd image, so please take this one

* Charge Type: currently I only finished PayByTraffic option

* Instance Charge Type: use PostPaid

* For the rest just leave default value

#### Starting create ECS instance

If your configurations are valid, you will see following message. That means, that Alibaba Cloud has received your request and start to create ECS instance.

```
Creating instance with following params ...
Region-ID: eu-central-1
InstanceName: ecs-ml-workstation
InstanceType : ecs.gn5-c4g1.xlarge
ZoneId : eu-central-1b
SecurityGroupId : sg-gw8##########
VSwitchId : vsw-gw89k0nq##########
KeyPairName : bai-mac
ImageId : ubuntu_18_04_x64_20G_alibase_20200220.vhd
InstanceName : ecs-ml-workstation
InternetChargeType : PayByTraffic
InternetMaxBandwidthOut : 25
InstanceChargeType : PostPaid
Period : 1
PeriodUnit : Hourly
Allocating public IP address ...
Attaching disks...
Instance public ip: 47.91.22.33
Starting ecs instance ...
Instance public ip: 47.91.22.33
```
### Check config.json file
This python program will generate or overwrite your local config.json file, which stores necessary informations for recreating instance. And it will also write your individual instance public ip address in "hosts" file (under playbook directory). ansible-playbook will use it to deploy things automatically in your remote ECS instance.

### Setup your data science workbench with ansible-playbook
The requirements.txt file contains ansible dependency, which means you can use command-line-tool ansible-playbook directly...

1. Checking if ECS instance is accessible

```
$ ansible all -m ping
```
2. Install deep learning libraries
```
$ ansible-playbook ecs-gpu-instance.yml
```

### Start jupyter notebook
Once your ansible-playbook is finished, you should do following steps to start jupyter server:

Login with ssh

```
$ ssh ml@(your ip)

# set password for jupyter remote login
$ jupyter notebook password
  Enter password:  ****
  Verify password: ****
  
# my ansible playbook has generated cert.pem and key.key for secured access
$ ml@iZgw89wtwllnq3g945jw7iZ:~/.jupyter$ jupyter notebook --certfile=mycert.pem --keyfile mykey.key
```

### Extra
After running nvidia_driver playbook, please login in your remote ECS instance by using **ssh ml@{ your ip address }** and verify driver installation via ```nvidia-smi``` command.
<br>
For example I choosed **cs.gn5-c4g1.xlarge** from catalog, which has **1 * NVIDIA P-100 GPU** processor and **1 * 16 GB GPU** memory:
```
$ ml@iZgw8hlwkk3wtun2uxt6pjZ:~$ nvidia-smi
```
Specially for installing nvidia driver see: https://github.com/NVIDIA/ansible-role-nvidia-driver

### More...
Currently we can use stop_ecs_instance.py to stop instance without deleting intance's network settings like VSwitch, VPC ... Deleting of these settings should also be included as optins in the future.
