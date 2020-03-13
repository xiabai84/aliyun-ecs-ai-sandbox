# aliyun-ecs-ai-sandbox

This is a automation script for building machine learning dev-environment on Alibaba Cloud, which is hosted in german region (Frankfurt am Main) by default setting.<br>

I use python for creating ECS instance. There is a ansible-playbook for installing nvidia drivers, libs for deep learning with GPU support. This guide assumes you will use ubuntu 18.04, the playbook may need some editing if you're using other versions of ubuntu or linux... 

### Deep Learning libraries

This script contains the newest version of tensorflow and pytorch.

* tensorflow 2.1, 
* tensorboard
* pytorch 1.4 
* torchvision
* jupyter
* cuda 10.2

It also provide a https user web interface by using jupyter server. You can access this development environment via https://< your public ip>:8888

### HandsOn - Setup EMS instance
1. Install python3 dependencies
Assume you already have virtualenvwrapper on your local machine.(https://virtualenvwrapper.readthedocs.io/en/latest/)
```
mkvirtualenv ali-cloud
pip install -r requirements.txt
```
2. Setup basic configurations in Alibaba Cloud
For remote access, you must generate ALIYUN_ACCESS_KEY_ID and ALIYUN_ACCESS_KEY_SECRET for your account. 
See: https://www.alibabacloud.com/help/doc-detail/142101.htm

3. Create ECS instance
Start init python script to create instance:
```
python setup_ecs_instance.py
```
* Enter ACCESS_KEY_ID and ACCESS_KEY_SECRET. You can find them unter User Management -> Security Management

* Choose region, where this instance should be started -> eu-central-1 is Frankfurt (Germany)

* Choose a instance type(hardware requirement). There are lots of available instance types. Because we want to achieve big work load in the cloud, I just contraint them to GPU instance. For example ecs.gn5-c4g1.xlarge. You can find detail description in their home page

* Then select disks and zone settings... You can just enter default "y", if you don't really familiar with such cloud configurations.

* For SecurityGroup I just use a basic configurations (http/https, ssh etc.) in order to access jupyter server web ui (port 8888)

* SSH KeyValue -> You need to generate your own id_rsa, id_rsa.pub and use id_rsa.pub for cloud KeyValue setting. For more information see https://www.alibabacloud.com/help/doc-detail/51793.html

* Choose base image for OS, all of installtion in the next steps are based on ubuntu_18_04_x64_20G_alibase_20200220.vhd image, so please use this one!

* Charge Type: currently I only finished PayByTraffic option

* Instance Charge Type: use PostPaid

* For the rest just use default value

#### Once it finished, you will see following message:
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
This python program will also generate or overwrite config.json, which stores informations for recreating instance. And it will also write the instance public ip address in "hosts" file (under playbook directory). ansible-playbook will use it to deploy everything you need automatically in your remote ECS instance.

### Setup your data science workbench with ansible-playbook
My requirements.txt file contains ansible dependency, which means you can use command-line-tool ansible-playbook directly...
1. Checking if ECS instance already exists
```
ansible all -m ping
```
2. Install deep learning libraries
```
ansible-playbook ecs-gpu-instance.yml
```
### Start jupyter notebook
Once your ansible-playbook finished, you should do following steps to start jupyter server:
Login with 
```
ssh ml@(your ip)

ml@iZgw89wtwllnq3g945jw7iZ:~/.jupyter$ jupyter notebook --certfile=mycert.pem --keyfile mykey.key
```
### Extra
After running nvidia_driver playbook, please login in your remote ECS instance by using **ssh ml@{ your ip address }** and verify driver installation via ```nvidia-smi``` command.
<br>
For example I choosed **cs.gn5-c4g1.xlarge** from catalog, which has **1 * NVIDIA P-100 GPU** processor and **1 * 16 GB GPU** memory:
```
ml@iZgw8hlwkk3wtun2uxt6pjZ:~$ nvidia-smi
```
Specially for installing nvidia driver see: https://github.com/NVIDIA/ansible-role-nvidia-driver

### More...
Currently we can use stop_ecs_instance.py to stop instance without deleting intance's network settings like VSwitch, VPC ... These features should also be included as optins during the deleting process in the future.
