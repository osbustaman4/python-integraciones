
import requests
import json

from flask import request, jsonify, Blueprint, current_app

from lib.Stech import Logger, Stech, Validate
from decouple import config as load_data

from datetime import datetime
from sqlalchemy import text, func

from src.utils.Utils import insert_integraciones_sinc


class IntegrationTMS():

    @classmethod
    def integration_tms(cls):
        try:
            with current_app.app_context():
                pass
            
        except Exception as e:
            return str(e)