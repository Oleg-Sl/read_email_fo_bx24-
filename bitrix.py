import requests
import json
import time
from pprint import pprint

import secrets


API = secrets.get_webhook() + "{method}.json"


def get_contact_by_email(email):
    method = "crm.contact.list"
    response = request_bx(method, {
        "filter": {"EMAIL": email},
        "select": ["*"]
    })
    if response and "result" in response:
        return response["result"]


def add_deal(fields):
    method = "crm.deal.add"
    response = request_bx(method, {
      "fields": fields,
      "params": {"REGISTER_SONET_EVENT": "Y"}
    })
    # pprint(response)
    if response and "result" in response:
        return response["result"]


# Запрос к Битрикс
def request_bx(method, data, count=5):
    timeout = 60
    try:
        url = API.format(method=method)
        headers = {
            'Content-Type': 'application/json',
        }
        r = requests.post(url, headers=headers, data=json.dumps(data), timeout=timeout)
        result = json.loads(r.text)
    except ValueError:
        result = dict(error='Error on decode api response [%s]' % r.text)
    except requests.exceptions.ReadTimeout:
        result = dict(error='Timeout waiting expired [%s sec]' % str(timeout))
    except requests.exceptions.ConnectionError:
        result = dict(error='Max retries exceeded [' + str(requests.adapters.DEFAULT_RETRIES) + ']')

    if r.status_code != 200:
        if count < 1:
            return
        time.sleep(1)
        return request_bx(method, data, count - 1)

    return result
