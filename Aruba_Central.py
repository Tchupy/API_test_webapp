from requests import request
import json
from menu import Menu
import time
from prettytable import PrettyTable

base_url = "https://eu-apigw.central.arubanetworks.com/"

def refresh_token():
    header = {
        'Content-Type': 'application/json'
    }

    with open('config.py','r+') as jfile:
        src_token = json.load(jfile)

    body_json = {
        "client_id": src_token['CLIENT_ID'],
        "client_secret": src_token['CLIENT_SECRET'],
        "grant_type": "refresh_token",
        "refresh_token": src_token['REFRESH_TOKEN']
    }

    api_url = "oauth2/token"
    req = request("POST", base_url + api_url, headers=header,data=json.dumps(body_json))

    # if expires_in = 7200 --> token has been refresh so update is needed
    if req.json()['expires_in'] == 7200:
        src_token['REFRESH_TOKEN'] = req.json()['refresh_token']
        src_token['ACCESS_TOKEN'] = req.json()['access_token']
        src_token['TIMESTAMP'] = int(time.time())
        with open('config.py', 'r+') as jfile:
            jfile.write(json.dumps(src_token, indent=2))

    return req.json()['access_token']

def get_token():
    with open('config.py','r') as jfile:
        src_token = json.load(jfile)
    # check if token is still valid or not
    if (int(time.time()) - src_token['TIMESTAMP']) > 7200:
        # token too old
        return refresh_token()
    else:
        # token is still valid
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

def get_devices(access_token)
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    api_url = "configuration/v1/devices/template_variables?offset=0&limit=20"
    req = request("GET", base_url + api_url, headers=header)



if __name__ == '__main__':
    token = get_token()
    m = Menu()
    m.add_field("Print devices list ")
    m.add_field("Print variables for all devices ")
    print(m)
    x = m.get_choice()
    if x == '2':
        print("get_var_all_devices")
        get_var_for_all_devices(token)
    elif x == '1':
        print("Print devices list")
