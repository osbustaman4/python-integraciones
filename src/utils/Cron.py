import json
import requests
import traceback

from src.api_integracion_tms import integration_tms
class Cron():

    @classmethod
    def integration_tms_01(self):
        url = "http://127.0.0.1:5000/integration-tms"

        payload = ""
        headers = {
        'Cookie': 'sessionid=a733msj76vgmd0j2dlulp0mgc49kk92r'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)