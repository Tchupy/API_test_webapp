from requests import request
from prettytable import PrettyTable
import json

def meraki_request(action, token, org_name='',org_id='', network_name='', network_id=''):
    '''

    :param action: ORG_LIST, ORG_ID, NET_LIST, NET_ID, DEVICES_LIST
    :param token:
    :param org_name:
    :param org_id:
    :param network_name:
    :param network_id:
    :return:
    '''
    base_url = "https://api.meraki.com/api/v1/"
    header = {
        'X-Cisco-Meraki-API-Key': token
    }
    if action == 'ORG_LIST':
        api_url = "organizations"
        r = request("GET", base_url + api_url, headers=header)
        return r.json()
    elif action == 'ORG_ID':
        api_url = "organizations"
        r = request("GET", base_url + api_url, headers=header)
        for org in r.json():
            if org['name'] == org_name:
                org_ID = org['id']
        return org_ID
    elif action == 'NET_LIST':
        if org_id=='':
            return "Error: org_id is empty"
        api_url = "organizations/" + org_id + "/networks"
        r = request("GET", base_url + api_url, headers=header)
        return r.json()
    elif action == 'NET_ID':
        if org_id == '' or network_name == '':
            return "Error: org_id or network_name is empty"
        api_url = "organizations/" + org_id + "/networks"
        r = request("GET", base_url + api_url, headers=header)
        net_ID = ""
        for network in r.json():
            if network['name'] == network_name:
                net_ID = network['id']
        return net_ID
    elif action == 'DEVICES_LIST':
        if network_id == '':
            return "Error: network_id  is empty"
        api_url = "networks/" + network_id + "/devices"
        r = request("GET", base_url + api_url, headers=header)
        return r.json()
    elif action == 'VLAN_LIST':
        if network_id == '':
            return "Error: network_id  is empty"
        api_url = "networks/" + network_id + "/appliance/vlans"
        r = request("GET", base_url+api_url, headers=header)
        return r.json()


'''

def get_orga(token, org_name):
    base_url = "https://api.meraki.com/api/v1/"
    api_url = "organizations"
    r = request("GET", base_url + api_url, headers=self.header)
    # get OrgID
    org_ID = ''
    print("org_name in get_orga function: " + org_name)
    for org in r.json():
        print(org)
        if org['name'] == org_name:
            org_ID = org['id']
    return org_ID

def get_orga_list(self):
    api_url = "organizations"
    r = request("GET", self.base_url + api_url, headers=self.header)
    return r.json()

    def set_orga(self, org_name):
        self.org_ID = self.get_orga(org_name)

    def get_network(self, net_name):
        # Get Network ID
        api_url = "organizations/" + self.org_ID + "/networks"
        r = request("GET", self.base_url+api_url, headers=self.header)
        net_ID = ""
        for network in r.json():
            #if network['name'] == "Massy OCWS - LABO":
            if network['name'] == net_name:
                net_ID = network['id']
        return net_ID

    def get_network_list(self):
        api_url = "organizations/" + self.org_ID + "/networks"
        r = request("GET", self.base_url + api_url, headers=self.header)
        return r.json()

    def set_network(self, net_name):
        self.net_ID = self.get_network(net_name)

    def get_devices(self, network_id=''):
        # GET /networks/:networkId/devices
        if network_id == '':
            network_id = self.net_ID
        api_url = "networks/" + network_id + "/devices"
        r = request("GET", self.base_url + api_url, headers=self.header)
        return r.json()

    def get_vlan_list(self, network_id=''):
        # list all VLANs in a network
        # https://api.meraki.com/api/v1/networks/:networkId/appliance/vlans
        if network_id == '':
            network_id = self.net_ID
        api_url = "networks/" + network_id + "/appliance/vlans"
        r = request("GET", self.base_url+api_url, headers=self.header)
        return r.json()

    def print_vlan_list(self, network_id=''):
        # print to console all VLANs in a network
        # https://api.meraki.com/api/v1/networks/:networkId/appliance/vlans
        if network_id == '':
            network_id = self.net_ID
        api_url = "networks/" + network_id + "/appliance/vlans"
        r = request("GET", self.base_url + api_url, headers=self.header)
        vlan_tab = PrettyTable()
        vlan_tab.field_names = ['VLAN Id', 'VLAN Name', 'Subnet', 'IP']
        for vlan in r.json():
            vlan_tab.add_row([vlan['id'], vlan['name'], vlan['subnet'], vlan['applianceIp']])
        print(vlan_tab)
        return

    def exist_network(self, network_id):
        # test if a network exists
        # GET/networks/{networkId}
        if network_id == '' or not isinstance(network_id, str):
            return False
        api_url = "networks/" + network_id
        r = request("GET", self.base_url + api_url, headers=self.header)
        if r.status_code == 200:
            # vlan exists
            return True
        elif r.status_code == 404:
            # vlan does not exist
            return False
        else:
            # error in request (authentication, url, etc..)
            # TODO
            return False

    def exist_vlan(self, vlan_id, network_id=''):
        # test if a vlan exists
        # GET/networks/{networkId}/appliance/vlans/{vlanId}

        if isinstance(vlan_id, int):
            vlan_id = str(vlan_id)
        if network_id == '':
            network_id = self.net_ID

        api_url = "networks/" + network_id + "/appliance/vlans/" + vlan_id
        r = request("GET", self.base_url + api_url, headers=self.header)
        if r.status_code == 200:
            # vlan exists
            return True
        elif r.status_code == 404:
            # vlan does not exist
            return False
        else:
            # error in request (authentication, url, etc..)
            # TODO
            return False

    def delete_vlan(self, vlan_id, network_id=''):
        # delete a vlan from a network
        # DELETE/networks/{networkId}/appliance/vlans/{vlanId}

        if isinstance(vlan_id, int):
            vlan_id = str(vlan_id)
        if network_id == '':
            network_id = self.net_ID

        if self.exist_vlan(vlan_id, network_id):
            api_url = "networks/" + network_id + "/appliance/vlans/" + vlan_id
            r = request("DELETE", self.base_url+api_url, headers=self.header)
            if r.status_code == 204:
                print("VLAN " + vlan_id + " has been removed")
                return 0
            else:
                print("VLAN " + vlan_id + "could not be removed. Does it exist ?" + str(r.status_code))
                return 1
        else:
            print("VLAN " + vlan_id + "does not exist in" + network_id)

    def add_vlan(self, vlan_id, vlan_name, vlan_subnet, vlan_ip, network_id=''):
        # add a vlan in a network
        # POST / networks / {networkId} / appliance / vlans

        if isinstance(vlan_id, int):
            vlan_id = str(vlan_id)
        if network_id == '':
            network_id = self.net_ID

        if not self.exist_vlan(vlan_id, network_id):
            api_url = "networks/" + network_id + "/appliance/vlans"
            parameters = {
                'id': vlan_id,
                'name': vlan_name,
                'subnet': vlan_subnet,
                'applianceIp': vlan_ip
            }
            r = request("POST", self.base_url+api_url, headers=self.header, params=parameters)
            if r.status_code == 201:
                print("\t\tVLAN " + vlan_id + " has been added")
                return True
            else:
                print("\t\tVLAN " + vlan_id + " could not be added.")
                return False
        else:
            print("\t\tVLAN " + vlan_id + " could not be added. Does it already exist ?")
            return False

    def bulk_add_vlan_from_file(self, filename):
        # VLAN creation from json file
        with open(filename) as vlan_file:
            vlan_json = json.load(vlan_file)

        for j_network in vlan_json:
            # try to create vlan for each networks
            if self.exist_network(j_network['network_id']):
                print("Processing network: " + j_network['network_id'])
                for j_vlan in j_network['vlans']:
                    self.add_vlan(j_network['network_id'], j_vlan['id'],j_vlan['name'], j_vlan['subnet'], j_vlan['applianceIp'])
            else:
                print("Network: " + j_network['network_id'] + " is unknown\n")

    def bulk_add_vlan_from_json(self, vlan_json):
        # VLAN creation from json file
        if not isinstance(vlan_json,list):
            print("Bad input format")
            return False

        # TODO : validate json format --> list of dict
        # TODO : 1 dict per network

        for j_network in vlan_json:
            # try to create vlan for each networks
            if self.exist_network(j_network['network_id']):
                print("Processing network: " + j_network['network_id'])
                for j_vlan in j_network['vlans']:
                    self.add_vlan(j_vlan['id'],j_vlan['name'], j_vlan['subnet'], j_vlan['applianceIp'],j_network['network_id'])
            else:
                print("Network: " + j_network['network_id'] + " is unknown\n")
                
'''