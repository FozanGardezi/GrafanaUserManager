import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


GRAFANA_USERNAME = settings.GRAFANA_USERNAME
GRAFANA_PASSWORD = settings.GRAFANA_PASSWORD
GRAFANA_URL = settings.GRAFANA_URL

def create_grafana_organization(org_name):
    url = f"{GRAFANA_URL}/orgs"
    data = {
        "name": org_name
    }
    response = requests.post(url, json=data, auth=HTTPBasicAuth(GRAFANA_USERNAME, GRAFANA_PASSWORD))
    response.raise_for_status()
    return response.json()

def update_grafana_organization(org_id, org_name):
    url = f"{GRAFANA_URL}/orgs/{org_id}"
    data = {
        "name": org_name
    }
    response = requests.put(url, json=data, auth=HTTPBasicAuth(GRAFANA_USERNAME, GRAFANA_PASSWORD))
    response.raise_for_status()
    return response.json() 

def delete_grafana_organization(org_id):
    url = f"{GRAFANA_URL}/orgs/{org_id}"
    response = requests.delete(url, auth=HTTPBasicAuth(GRAFANA_USERNAME, GRAFANA_PASSWORD))
    response.raise_for_status()
    return response.status_code


def create_grafana_user(name, email, login, password, org_id):
    grafana_url = f"{GRAFANA_URL}/admin/users"

    grafana_auth = (grafana_username, grafana_password)
    grafana_data = {
        "name": name,
        "email": email,
        "login": login,
        "password": password,
        "orgId": org_id,
    }
    response = requests.post(grafana_url, json=grafana_data, auth=grafana_auth)
    return response.json() if response.status_code == 200 else None

def update_grafana_user(grafaid, name, email, login, org_id):
    grafana_url = f"{GRAFANA_URL}/admin/users/{grafaid}"

    grafana_auth = (grafana_username, grafana_password)
    grafana_data = {
        "name": name,
        "email": email,
        "login": login,
        "orgId": org_id,
    }
    response = requests.put(grafana_url, json=grafana_data, auth=grafana_auth)
    return response.status_code == 200

def delete_grafana_user(grafaid):
    grafana_url = f"{GRAFANA_URL}/admin/users/{grafaid}"
    grafana_auth = (grafana_username, grafana_password)
    response = requests.delete(grafana_url, auth=grafana_auth)
    return response.status_code == 200
