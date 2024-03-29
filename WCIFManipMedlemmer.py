import subprocess
from datetime import timedelta
from copy import deepcopy
from time import sleep
import json
import requests
import pytz
from pandas import Timestamp
import os

def get_data_from_wcaid(wcaid):
    response = requests.get(f"https://api.worldcubeassociation.org/users/{wcaid}")
    # assert response.status_code == 200, f"Failed wcaid: {wcaid}, code: {response.status_code}"
    if response.status_code ==200:
        content = json.loads(response.content)['user']
        return 200, (content['id'],content['name'],content['wca_id'])

    return response.status_code,(None,None,None)

def get_me(header):
    return requests.get("https://api.worldcubeassociation.org/me",headers=header)

def get_coming_comps(header,userid):
    fromDate = (Timestamp.now() - timedelta(days=5))._date_repr
    comps_json = json.loads(requests.get(f"https://api.worldcubeassociation.org/competitions?managed_by_me=true&start={fromDate}",headers=header).content)
    comps=  [(comp['name'],comp['id'],True,comp['end_date']) for comp in comps_json]
    regged_comps_json = json.loads(requests.get(f"https://api.worldcubeassociation.org/users/{userid}?upcoming_competitions=true&ongoing_competitions=true",headers=header).content)
    upcoming = regged_comps_json['upcoming_competitions']
    ongoing = regged_comps_json['ongoing_competitions']
    # print(regged_comps_json['user'].keys())
    
    comps = comps + [(comp['name'],comp['id'],False,comp['end_date']) for comp in upcoming if (comp['name'],comp['id'],True,comp['end_date']) not in comps]
    comps = comps + [(comp['name'],comp['id'],False,comp['end_date']) for comp in ongoing if (comp['name'],comp['id'],True,comp['end_date']) not in comps]
    comps.sort(key=lambda x:x[3])
    return comps
# https://www.worldcubeassociation.org/api/v0/users/6777?upcoming_competitions=true&ongoing_competitions=true
# https://www.worldcubeassociation.org/api/v0/competitions?managed_by_me=true&start=2022-12-31


def getWcif(id,header):
    wcif = requests.get(f"https://api.worldcubeassociation.org/competitions/{id}/wcif",headers=header)
    # assert wcif.status_code == 200
    return json.loads(wcif.content),wcif.status_code

def getWCIFPublic(id):
    wcif = requests.get(f"https://api.worldcubeassociation.org/competitions/{id}/wcif/public")
    return json.loads(wcif.content),wcif.status_code

def get_competitors_wcif(id):
    wcif, _ = getWCIFPublic(id)
    competitors = [person['wcaUserId'] for person in wcif['persons']]
    return competitors

def get_comming_danish_comps():
    from_date = (Timestamp.now() - timedelta(days=5))._date_repr
    comps = json.loads(requests.get(f"https://api.worldcubeassociation.org/competitions?country_iso2=DK&start={from_date}").content)
    comps_short = [(comp['name'],comp['id'],False,comp['end_date']) for comp in comps]
    comps_short.sort(key=lambda x:x[3])
    return comps_short
