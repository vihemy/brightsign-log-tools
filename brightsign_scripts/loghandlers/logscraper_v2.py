import requests
import json
import webbrowser

def main(players):
    # gets dictionary players from index file through read_brightsign_index()
    for value in players.values():
        ip = value[0] # gets ip from dict-value
        try:
            json_data = json_from_url(ip)
        except requests.Timeout as err:
            print(f"\nCould not connect to player with ip: {ip}")
            continue
        try:
            log_name_list = log_name_list_from_json(json_data)
        except KeyError as err:
            print(f"\nNo logs found on player with ip: {ip}")
            continue
        
        download_logs_from_list(log_name_list, ip)
        print(f"\nDownload of player with ip: {ip} complete")

#for trying indivual ip's
def semi_main():
    ip = "10.0.1.115"
    json_data = json_from_url(ip)
    log_name_list = log_name_list_from_json(json_data)
    download_logs_from_list(log_name_list, ip)
    

def json_from_url(ip):
    #creates device_url
    device_url = "http://" + ip + "/api/v1/files/sd/logs/"
    #gets json from url
    r = requests.get(device_url)
    t = r.text
    json_data = json.loads(t)
    return json_data

def log_name_list_from_json(data):
    # counts nr of logentries
    logs = data['data']['result']['files']
    log_count = len(logs)
    log_name_list = []
    x=1
    for x in range(log_count):
        log_name_list.append(data['data']['result']['files'][x]['name'])
        x+=1
    return log_name_list

def download_logs_from_list(log_name_list, ip):
    #url parts
    url_prefix = "http://"
    url_infix = "/api/v1/files/sd/logs/"
    url_suffix ="?contents&stream"
    #url_eksempel: "http://10.0.1.115/api/v1/files/sd/logs/BrightSignLog.TKD1CN002225-220919000.log?contents&stream"
    for log_name in log_name_list:
        download_url = url_prefix + ip + url_infix + log_name + url_suffix
        webbrowser.open(download_url)
