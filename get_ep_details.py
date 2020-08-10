from connectivity import get_aci_token
from credentials import credentials
import json
import requests
from pprint import pprint
from prettytable import PrettyTable 


def get_ep_details(aci_cookie, apic_ip,mac_addr=None):
    ######### GET EP Details ##############
    # GET EP details

    if mac_addr:
        url = f'{apic_ip}/api/node/class/fvCEp.json?query-target-filter=and(wcard(fvCEp.mac,"{mac_addr}"))&order-by=fvCEp.modTs|desc'
    else:
        url = f'{apic_ip}/api/node/class/fvCEp.json?&order-by=fvCEp.modTs|desc'

    headers = {
        'cache-control': "no-cache"
    }

    get_response = requests.get(
        url, headers=headers, cookies=aci_cookie, verify=False).json()

    return get_response


if __name__ == '__main__':
    mac_addr = input("Enter full or part of mac address in format AA:BB:CC:DD:EE:FF or leave blank to show all results. : ")
    aci_cookie = get_aci_token(
        credentials["username"], credentials["password"], credentials["apic_ip"])
    get_ep_details_result = get_ep_details(aci_cookie, credentials["apic_ip"],mac_addr.upper())
    
    # pprint(get_ep_details_result)

    fields = ['mac', 'ip','encap','dn']
    data = []

for endpoints in get_ep_details_result['imdata']:
    for endpoint_data in endpoints['fvCEp'].items():
        line_dict={}
        for field in fields:
            line_dict[field] = endpoint_data[1][field]
        data.append(line_dict)

table = PrettyTable()
table.field_names = ['MAC Address','VLAN','Tenant','AP','EPG']
for row in data:
    dn_splitted_list = row['dn'].split("/")
    mac = row['mac']
    vlan = row['encap'].lstrip("vlan-")
    tenant = dn_splitted_list[1].lstrip("tn-")
    ap = dn_splitted_list[2].lstrip("ap-")
    epg = dn_splitted_list[3].lstrip("epg-")
    

    table.add_row([mac,vlan,tenant,ap,epg])

print(table)
