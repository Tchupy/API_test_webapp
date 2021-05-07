from requests import request
import json
from menu import Menu
import time
from prettytable import PrettyTable

base_url = "https://eu-apigw.central.arubanetworks.com/"

def refresh_token():
    if 'DEBUG' in locals() and DEBUG:
        central_log.info("in refresh_token")
    header = {
        'Content-Type': 'application/json'
    }

    with open('config_token.json', 'r+') as jfile:
        src_token = json.load(jfile)

    body_json = {
        "client_id": src_token['CLIENT_ID'],
        "client_secret": src_token['CLIENT_SECRET'],
        "grant_type": "refresh_token",
        "refresh_token": src_token['REFRESH_TOKEN']
    }

    api_url = "oauth2/token"
    req = request("POST", base_url + api_url, headers=header,data=json.dumps(body_json))

    if req.status_code == 200:
        # if expires_in = 7200 --> token has been refresh so update is needed
        if req.json()['expires_in'] == 7200:
            src_token['REFRESH_TOKEN'] = req.json()['refresh_token']
            src_token['ACCESS_TOKEN'] = req.json()['access_token']
            src_token['TIMESTAMP'] = int(time.time())
            with open('config.py', 'r+') as jfile:
                jfile.write(json.dumps(src_token, indent=2))
            if DEBUG:
                central_log.info("in refresh_token: token written to file")
        return req.json()['access_token']
    else:
        if 'DEBUG' in locals() and DEBUG:
            central_log.info("in refresh_token: get_new_token. req status_code:" + req.status_code)
        return get_new_token()

def get_token():
    with open('config_token.json','r') as jfile:
        src_token = json.load(jfile)
    # check if token is still valid or not
    if (int(time.time()) - src_token['TIMESTAMP']) > 7200:
        # token too old
        if 'DEBUG' in locals() and DEBUG:
            central_log.info("in get_token: access new Token")
        return refresh_token()
    else:
        # token is still valid
        if 'DEBUG' in locals() and DEBUG:
            central_log.info("in get_token: token is valid")
        return src_token['ACCESS_TOKEN']

def get_var_for_device(Serial,access_token):
    # "CN72HKZ00K"
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    api_url = "configuration/v1/devices/" + Serial + "/template_variables?offset=0&limit=20"
    req = request("GET", base_url + api_url, headers=header)
    print("Variables list for device " + req.json()['device_serial'] + ": \n")
    '''
    var_tab = PrettyTable()
    var_tab.field_names = ["Variable", "Value"]
    for item in req.json()['data']['variables']:
        var_tab.add_row([item,req.json()['data']['variables'][item]])
    print(var_tab)'''
    print(json.dumps(req.json()['data']['variables'],indent=2))

def get_var_for_all_devices(access_token):

    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    api_url = "configuration/v1/devices/template_variables?offset=0&limit=20"
    req = request("GET", base_url + api_url, headers=header)
    print("Variables list: \n")
    '''
    var_tab = PrettyTable()
    var_tab.field_names = ["Variable", "Value"]
    for item in req.json()['data']['variables']:
        var_tab.add_row([item,req.json()['data']['variables'][item]])
    print(var_tab)'''
    print(json.dumps(req.json(),indent=2))

def get_devices(access_token):
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    api_url = "configuration/v1/devices/template_variables?offset=0&limit=20"
    req = request("GET", base_url + api_url, headers=header)


def get_switches(access_token):
    '''
    get list of switches in customer ID

    :param access_token: valid access token
    :return: json data

    JSON data returned has following format
        { 'count': switch_number,
           'switches' : [ list of switches_dict]
        }
        switches_dict has these keys :
        { firmware_version / group_id / ip_address / label_ids / labels / macaddr / model / name / public_ip_address /
        serial / site / site_id / stack_id / status / switch_type / uplink_ports / usage }
    '''
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    api_url = "monitoring/v1/switches"
    req = request("GET", base_url + api_url, headers=header)
    return req.json()

def get_aps(access_token):
    '''
    get list of aps

    :param access_token:
    :return: json data

    JSON data returned has following format
        { 'aps': [ list of ap_dict ]
        }
    ap_dict has following keys:
    ip_address / macaddr / model / name / public_ip_address / serial / site / status / swarm_master / swarm_name

    '''
    api_url = "monitoring/v1/aps"
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    req = request("GET", base_url + api_url, headers=header)
    return req.json()

