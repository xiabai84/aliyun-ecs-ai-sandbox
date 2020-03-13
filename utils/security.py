import os
import time

from aliyunsdkecs.request.v20140526 import (
    CreateSecurityGroupRequest,
    DescribeSecurityGroupsRequest,
    AuthorizeSecurityGroupRequest,
    CreateVpcRequest,
    CreateVSwitchRequest,
    DescribeVSwitchesRequest,
    DescribeKeyPairsRequest,
    ImportKeyPairRequest,
)

from .action import do_action
from .select import BaseConfigParameterSelect


class SecurityGroupsSelect(BaseConfigParameterSelect):
    name = "SecurityGroup"
    key = ['CreateInstanceParams', 'SecurityGroupId']
    request_cls = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest
    items_getter = lambda self, x: x['SecurityGroups']['SecurityGroup']
    item_key = "SecurityGroupId"
    select_item_formatter = lambda self, x: "{}({})".format(x['SecurityGroupName'], x['SecurityGroupId'])

    def handle_selected_item(self, item):
        self.set_VSwitchId(item['VpcId'])

    def fix_empty_items(self):
        # 因为创建安全组时需要指定 VpcId, 这里偷个懒， 假定安全组为空时， vpc 和 vswitch
        # 也为空， 创建一个新的
        print('Creating VPC, please wait ...')
        self.create_vpc()
        print('Creating VSwitch, please wait ...')
        time.sleep(5)
        self.create_vswitch()
        print('Creating SecurityGroup, plase wait ...')
        self.create_sg()
        time.sleep(5)
        print('Createing SecurityGroup Rules, please wait ...')
        self.add_sg_rule()
        time.sleep(5)
        self.add_sg_http_rule()
        time.sleep(5)
        self.add_sg_https_rule()
        time.sleep(5)
        self.add_sg_ssh_rule()
        time.sleep(5)
        self.add_sg_icmp_rule()
        time.sleep(5)

    def create_sg(self):
        request = CreateSecurityGroupRequest.CreateSecurityGroupRequest()
        request.set_VpcId(self.VpcId)
        result = do_action(self.client, request)
        self.SecurityGroupId = result['SecurityGroupId']

    def add_sg_rule(self):
        # Adding SecurityGroup for Jupyter Notebook
        request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
        request.set_IpProtocol("tcp")
        request.set_PortRange("8888/8888")
        request.set_SecurityGroupId(self.SecurityGroupId)
        request.set_SourceCidrIp('0.0.0.0/0')
        result = do_action(self.client, request)
        for param_name, param_value in result.items():
            print(f"sg-jupyter-setting: {param_name} - {param_value}")
    
    def add_sg_http_rule(self):
        request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
        request.set_IpProtocol("tcp")
        request.set_PortRange("80/80")
        request.set_SecurityGroupId(self.SecurityGroupId)
        request.set_SourceCidrIp('0.0.0.0/0')
        result = do_action(self.client, request)
        for param_name, param_value in result.items():
            print(f"sg-http-setting: {param_name} - {param_value}")
    
    def add_sg_https_rule(self):
        request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
        request.set_IpProtocol("tcp")
        request.set_PortRange("443/443")
        request.set_SecurityGroupId(self.SecurityGroupId)
        request.set_SourceCidrIp('0.0.0.0/0')
        result = do_action(self.client, request)
        for param_name, param_value in result.items():
            print(f"sg-https-setting: {param_name} - {param_value}")

    def add_sg_ssh_rule(self):
        request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
        request.set_IpProtocol("tcp")
        request.set_PortRange("22/22")
        request.set_SecurityGroupId(self.SecurityGroupId)
        request.set_SourceCidrIp('0.0.0.0/0')
        result = do_action(self.client, request)
        for param_name, param_value in result.items():
            print(f"sg-ssh-setting: {param_name} - {param_value}")

    def add_sg_icmp_rule(self):
        request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
        request.set_IpProtocol("icmp")
        request.set_PortRange("-1/-1")
        request.set_SecurityGroupId(self.SecurityGroupId)
        request.set_SourceCidrIp('0.0.0.0/0')
        result = do_action(self.client, request)
        for param_name, param_value in result.items():
            print(f"sg-icmp-ipv4-setting: {param_name} - {param_value}")

    def create_vpc(self):
        request = CreateVpcRequest.CreateVpcRequest()
        request.set_VpcName('ecs-ml-auto-vpc')
        request.set_CidrBlock('192.168.0.0/16')
        result = do_action(self.client, request)
        self.VpcId = result['VpcId']

    def create_vswitch(self):
        request = CreateVSwitchRequest.CreateVSwitchRequest()
        request.set_CidrBlock('192.168.0.0/24')
        request.set_VpcId(self.VpcId)
        ZoneId = self.config.get(['CreateInstanceParams', 'ZoneId'])
        request.set_ZoneId(ZoneId)
        result = do_action(self.client, request)
        for param_name, param_value in result.items():
            print(f"vswitch-setting: {param_name} - {param_value}")

    def set_VSwitchId(self, vpc_id):
        request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
        request.set_VpcId(self.VpcId)
        result = do_action(self.client, request)
        item = result['VSwitches']['VSwitch'][0]
        self.config.set(['CreateInstanceParams', 'VSwitchId'], item['VSwitchId'])


class KeyPairsSelect(BaseConfigParameterSelect):
    name = "SSH KeyValue pair"
    key = ['CreateInstanceParams', 'KeyPairName']
    request_cls = DescribeKeyPairsRequest.DescribeKeyPairsRequest
    items_getter = lambda self, x: x['KeyPairs']['KeyPair']
    item_key = "KeyPairName"
    select_item_formatter = lambda self, x: x['KeyPairName']

    def fix_empty_items(self):
        self.import_key()

    def import_key(self):
        request = ImportKeyPairRequest.ImportKeyPairRequest()
        request.set_KeyPairName('ml-sshkey')
        key_path = os.path.expanduser('~/.ssh/id_rsa.pub')
        with open(key_path) as f:
            keybody = f.read()

        request.set_PublicKeyBody(keybody)
        do_action(self.client, request)
