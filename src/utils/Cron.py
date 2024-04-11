import json
import requests
import traceback

from sqlalchemy import text
from decouple import config as load_data
from lib.Stech import Stech
from src.api_integracion_tms import IntegrationTMS
from src.integrations.IntegrationTms import IntegrationTms
from src.utils.Utils import insert_integraciones_sinc

class Cron():

    @classmethod
    def integration_tms_01(self):
        try:
            IntegrationTms.integration_tms_01()
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())
            pass
