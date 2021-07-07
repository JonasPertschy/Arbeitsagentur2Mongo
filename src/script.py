import requests
import json
import pymongo
from tqdm import tqdm

myclient = pymongo.MongoClient("mongodb://[REDACTED]:27017/")
mydb = myclient["[REDACTED]"]
mycol = mydb["arbeitsagentur"]

''' Uncomment if you have pushover, like me. Its an amazing deal!
def pushover(msg):
    print(msg)
    try:
        if json.loads(requests.post("https://api.pushover.net/1/messages.json", data = {
            "token": "[REDACTED]",
            "user": "[REDACTED]",
            "message": msg
        }).text)['status'] == 1:
            return True
        else:
            return False
    except:
        print("Pushover ERROR")
        return False
'''
def pushover(msg):
    print(msg)

def get_token():
    # Request (2)
    # POST https://api-con.arbeitsagentur.de/oauth/gettoken_cc

    try:
        response = requests.post(
            url="https://api-con.arbeitsagentur.de/oauth/gettoken_cc",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
                "Origin": "https://con.arbeitsagentur.de",
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            },
            data={
                "grant_type": "client_credentials",
                "client_id": "dcdeacbd-2b62-4261-a1fa-d7202b579848",
                "client_secret": "9b24cdad-5323-4c7a-a4cb-cf0e6db04958",
            },
        )
        if response.status_code==200:
            return json.loads(response.content)['access_token']
        else:
            pushover("ERROR: get_token Cannot get token")
            return False
    except:
        pushover("ERROR: get_token Cannot get token Request failed")
        return False

def get_jobs(auth_token,pagination=1):
    # Request
    # GET https://api-con.arbeitsagentur.de/prod/jobboerse/jobsuche-service/pc/v3/jobs

    try:
        response = requests.get(
            url="https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
                "Origin": "https://con.arbeitsagentur.de",
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "OAuthAccessToken": "Bearer "+auth_token,
            },
            params={
                "angebotsart":"1",
                "wo":"76316",
                "umkreis":"25",
                "page":pagination,
                "size":"100",
                "pav":"false"
            },
            #proxies={'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080'}, verify=False
        )
        print(response.text)
        if response.status_code==200:
            #print(response.content)
            if '_embedded' in json.loads(response.content):
                for job in json.loads(response.content)['_embedded']['jobs']:
                    if 'jobdetails' in job['_links'] and 'freieBezeichnung' in job:
                        job['seen'] = False
                        try:
                            mycol.insert(job)
                            print(job['freieBezeichnung'],'added')
                        except pymongo.errors.DuplicateKeyError:
                            print(job['freieBezeichnung'],'in database')
                            pass
                if not json.loads(response.content)['page']['number']+1 >= json.loads(response.content)['page']['totalPages']:
                    return get_jobs(auth_token,json.loads(response.content)['page']['number']+1)
                else:
                    return True
            else:
                return True
        else:
            pushover("ERROR: get_jobs Cannot get data")
            return False
    except requests.exceptions.RequestException:
        pushover('get_jobs HTTP Request failed')
        return False


auth_token = get_token()
if auth_token:
    get_jobs(auth_token)