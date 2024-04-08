import base64
import json
import random
import tempfile
import traceback
import os
import requests
import hashlib
import hmac

from datetime import date, datetime, timedelta
from decouple import config as load_data
from flask import request, jsonify, Blueprint
from lib.Email import EmailSender
from lib.ExceptionsHTTP import HTTP404Error
from lib.Stech import Logger, Stech, Validate
from lib.ExceptionsJson import ExceptionsJson

from src.decorators import verify_user_fcm
from sqlalchemy import desc, literal
from sqlalchemy import Integer, String, update, func, and_, or_, case, Date, cast, literal_column, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import aliased
from src.models.recuperautos.Auditoria import Auditoria

from datetime import datetime

f
from src.utils.FCM import send_push_notification
from src.utils.Utils import Utils, Utils_Mails

#main_funcion_ejemplo = Blueprint('funcion_ejemploc', __name__)



@main_funcion_ejemplo.route('/', methods=['POST'])
@verify_user_fcm
def funcion_ejemplo():s
    try:
    
        session = Stech.get_session(load_data('ENVIRONMENTS'))
        data = request.get_json()
        error_validate, is_validate = Validate.validate_json_keys(data)
        if is_validate:
            raise ValueError(error_validate)
        
        response_whitelist_code_information, code_status = Utils.whitelist_code_information(data)
        
        if response_whitelist_code_information["tipocod"] == "EMPRESA":
            
            data["infocod"] = response_whitelist_code_information["infocod"]
            response_new_license_code_company, number_response = Utils.new_license_code_company(data)

            if not number_response == 400:

                if response_new_license_code_company["devrec"]:
                    data["devrec"] = response_new_license_code_company["devrec"]    
                    data["action"] = 1

                    data_recover_reward, number_error_recover_reward = Utils.recover_reward(data)

                    if number_error_recover_reward == 200:
                        data["more"] = data_recover_reward

                        send_mail = Utils.email_request_return_reward(data)

                        if not send_mail["success"]:
                            response = {
                                "success": False,
                                "message": "Correo no enviado correctamente"
                            }
                            return jsonify(response), send_mail["response_http"]
                        
                        else:
                            response = {
                                "success": True,
                                "message": "Correo enviado correctamente"
                            }
                            return jsonify(response), send_mail["response_http"]
                else:

                    data_new_code_license_company, number_new_code_license_company = Utils.email_new_code_license_company(data)

                    if number_new_code_license_company == 200:
                        response = {
                            "success": True,
                            "message": "Correo enviado correctamente"
                        }
                        return jsonify(response), 200
                    
                    else:
                        response = {
                            "success": False,
                            "message": "Correo no enviado correctamente"
                        }
                        return jsonify(response), 400

        else:
            response_code_license = Utils.new_code_license(data)

            if response_code_license:
                response = {
                    "success": True,
                    "message": "Codigo Recuperauto creado correctamente"
                }
                return jsonify(response), 200
            

        response = {
            "success": True
        }
        return jsonify(response), 200

    except ValueError as ex:
        return Utils.create_response(str(ex), False, 404)

    except SQLAlchemyError as ex:
        return Utils.create_response(str(ex), False, 500)

    except Exception as ex:
        message = f"{str(ex)} - {str(traceback.format_exc())}"
        return Utils.create_response(message, False, 500)
    

