import requests
import configparser
import json
import os
from datetime import date


config = configparser.ConfigParser()
config.read('config.conf')

subdom_list = ['.github.io','.animaapp.com','.bitbucket.io','.cargocollective.com','.createsend.com','.feedpress.me','.helpjuice.com', '.helpscoutdocs.com',
               '.intercom.help', '.myjetbrains.com', '.kinsta.cloud', '.launchrock.com', 'stats.uptimerobot.com', '.surge.sh', '.hatenablog.com', '.readme.io', 's3.amazonaws.com']
edge_list = ['.unbouncepages.com', '.map.fastly.net', '.netlify.com', '.netlify.app', '.webflow.com', '.webflow.io', '.cname.ngrok.io']


result_confirm = {}

result_edge = {}

CF_APIKEY = os.getenv("CF_APIKEY")
CF_EMAIL = config['Properties']['CF_EMAIL']
Notification_Mode = config['Properties']['Monitor_Mode']
slack_integration = config['Properties']['slack_integration']
if slack_integration == "true":
    slack_webhookURL = config['Properties']['slack_Webhook']

CF_MonitorSingleAccount = config['Properties']['CF_MonitorSingleAccount']
SoloMode = 0
CF_AccountID = ''
cnameList = []
zoneList = []

msg1 = "[+]Dangling Subdomains which might be vulnerable to takeover(EDGE CASE) :"
msg2 = "[+]Dangling Subdomains which are vulnerable to takeover :"


if CF_MonitorSingleAccount == "true":
    SoloMode = 1
    CF_AccountID = config['Properties']['CF_AccountID']

CF_headers = {
    'Content-Type': 'application/json',
    'X-Auth-Email' : CF_EMAIL,
    'X-Auth-Key' : CF_APIKEY
}

slack_headers = {
'Content-Type': 'application/json'
}

def getActiveZones():
    getZOneEndpoint = "https://api.cloudflare.com/client/v4/zones"
    if SoloMode == 1:
        query = {'status': 'active', 'account.id': CF_AccountID,'match': 'all'}
    else:
        query = {'status': 'active'}
    response = requests.request(method='GET', url=getZOneEndpoint, params=query, headers=CF_headers)
    jsonResp = json.loads(response.text)

    if jsonResp['result_info']['total_pages'] != 0:
        num_pages = jsonResp['result_info']['total_pages']
        for x in range(1,num_pages+1):
            new_query = query
            new_query['page'] = x
            response2 = requests.request(method='GET', url=getZOneEndpoint, params=new_query, headers=CF_headers)
            jsonResp2 = json.loads(response2.text)
            for y in range(0,len(jsonResp2['result'])):
                zoneList.append(jsonResp2['result'][y]['id'])
    else:
        print("[-]No zones found for the following account.")
        exit()

def validateCNAME():
    cname_query = {'type': 'CNAME'}
    global result_confirm, result_edge

    for record in zoneList:
        RecID = record
        DNSEndpoint = "https://api.cloudflare.com/client/v4/zones/" + record + "/dns_records"
        response = requests.request(method='GET', url=DNSEndpoint, params=cname_query, headers=CF_headers)
        jsonResp = json.loads(response.text)

        if "total_count" in jsonResp["result_info"]:
            if jsonResp["result_info"]["total_count"] != 0:
                num_pages = jsonResp['result_info']['total_pages']
                for x in range(1, num_pages + 1):
                    new_query2 = cname_query
                    new_query2['page'] = x
                    response2 = requests.request(method='GET', url=DNSEndpoint, params=new_query2,headers=CF_headers)
                    jsonResp2 = json.loads(response2.text)
                    for z in range(0, len(jsonResp2['result'])):
                        for slist in subdom_list:
                            if slist in jsonResp2["result"][z]["content"]:
                                url1 = 'https://' + jsonResp2["result"][z]["name"]
                                try:
                                    resp = requests.request(method='GET', url=url1, verify=False)
                                    if resp.status_code == 404:
                                        print("CNAME RECORD : " + jsonResp2["result"][z]["name"] + " Value: " +
                                            jsonResp2["result"][z]["content"])
                                        print("sub domain is vulnerable to takeover:", url1)
                                        result_confirm[jsonResp2["result"][z]["name"]] = jsonResp2["result"][z]["content"]

                                except requests.ConnectionError:
                                    print("[-]Unable to connect to the subdomain.")
                                    continue

                        for vlist in edge_list:
                            if vlist in jsonResp2["result"][z]["content"]:
                                url1 = 'https://' + jsonResp2["result"][z]["name"]
                                try:
                                    resp = requests.request(method='GET', url=url1, verify=False)
                                    if resp.status_code == 404:
                                        print("CNAME RECORD : " + jsonResp2["result"][z]["name"] + " Value: " +
                                            jsonResp2["result"][z]["content"])
                                        print("Sub domain might be vulnerable to takeover(EDGE CASE):",url1,"\n")
                                        result_edge[jsonResp2["result"][z]["name"]] = jsonResp2["result"][z]["content"]

                                except requests.ConnectionError:
                                    print("[-]Unable to connect to the subdomain.")
                                    continue

        else:
            print("\n[-]Something Wrong. Please try again later.\n")
            exit()


def SendSLackMessage(result,msgtype):

    if len(result) > 0:
        today = date.today()
        Msg1 = "Scan Date : "+ str(today) + "\n" + "*"+msgtype+"*"+"\n"
        data = {
        "text": Msg1
        }
        resp = requests.request(method='POST', url=slack_webhookURL, headers=slack_headers,json=data)
        for key in result.keys():
            Msg2 = "[+]Subdomain : "+ key + " " + "points to dangling pointer/value : " + result[key]
            data2 ={"text":Msg2}
            resp = requests.request(method='POST', url=slack_webhookURL, headers=slack_headers, json=data2)


def parseResult():
    if len(result_edge) > 0:
        if Notification_Mode == "1":
            if slack_integration == "true":
                SendSLackMessage(result_edge,msg1)
        if Notification_Mode == "2":
            if os.path.exists('edgecases.json') == False:
                if slack_integration == "true":
                    SendSLackMessage(result_edge, msg1)
            else:
                with open('edgecases.json', 'r') as fp1:
                    exist_list_edge = json.load(fp1)
                new_edge = {}
                for key in result_edge.keys():
                    if not key in exist_list_edge:
                        new_edge[key] = result_edge[key]
                if slack_integration == "true":
                    SendSLackMessage(new_edge, msg1)
        with open('edgecases.json', 'w') as wp1:
            json.dump(result_edge, wp1)
    else:
        if os.path.exists('edgecases.json') == True:
            os.remove("edgecases.json")


    if len(result_confirm) > 0:
        if Notification_Mode == "1":
            if slack_integration == "true":
                SendSLackMessage(result_confirm, msg2)
        if Notification_Mode == "2":
            if os.path.exists('vulnerable.json') == False:
                if slack_integration == "true":
                    SendSLackMessage(result_confirm, msg2)
            else:
                with open('vulnerable.json', 'r') as fp2:
                    exist_list_confirm = json.load(fp2)
                new_confirm = {}
                for key in result_confirm.keys():
                    if not key in exist_list_confirm:
                        new_confirm[key] = result_confirm[key]
                if slack_integration == "true":
                    SendSLackMessage(new_confirm, msg2)
        with open('vulnerable.json', 'w') as wp2:
            json.dump(result_confirm, wp2)
    else:
        if os.path.exists('vulnerable.json') == True:
            os.remove("vulnerable.json")


if __name__ == "__main__":
    print('''
                 _   _   _______    _                            
     /\         | | (_) |__   __|  | |                           
    /  \   _ __ | |_ _     | | __ _| | _____  _____   _____ _ __ 
   / /\ \ | '_ \| __| |    | |/ _` | |/ / _ \/ _ \ \ / / _ \ '__|
  / ____ \| | | | |_| |    | | (_| |   <  __/ (_) \ V /  __/ |   
 /_/    \_\_| |_|\__|_|    |_|\__,_|_|\_\___|\___/ \_/ \___|_|   
                                                                 
                                                                 @barriersec.com''')
    print("[+]Fetching Zone List....")
    getActiveZones()
    print("[+]Validating CNAME Records....")
    validateCNAME()
    print("[+]Parsing result.....")
    parseResult()

