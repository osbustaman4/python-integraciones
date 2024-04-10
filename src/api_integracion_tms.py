
import requests
import json

from flask import request, jsonify, Blueprint

from lib.Stech import Logger, Stech, Validate
from decouple import config as load_data

from datetime import datetime
from sqlalchemy import text, func

from src.utils.Utils import insert_integraciones_sinc

main_integration_tms = Blueprint('main_integration_tms', __name__)

@main_integration_tms.route('/', methods=['GET'])
def integration_tms():
    try:
        session = Stech.get_session(load_data('ENVIRONMENTS'))

        result_time_zone= session.execute(text("""SELECT timezone FROM gs_users WHERE id = 1;"""))

        response_data_timezone = [
            {
                "timezone": result.timezone,
            }
            for result in result_time_zone
        ]
        
        
        query_results = session.execute(text(f"""
            SELECT
                obj.plate_number AS patente,
                obj.lat AS latitude,
                obj.lng AS longitude,
                DATE_SUB( obj.dt_tracker, INTERVAL {response_data_timezone[0]["timezone"]} ) AS date_time,
                obj.speed,
                obj.dt_tracker,
                obj.dt_server,
                obj.params,
                obj.angle,
                CASE
                    IFNULL( JSON_EXTRACT( obj.params, '$.io1' ), '' ) 
                    WHEN '' THEN
                    JSON_EXTRACT( obj.params, '$.io239' ) 
                END AS acc,
                'stech' AS empresa_proveedora_gps,
                obj.imei
            FROM
                gs_objects obj
                JOIN gs_user_objects u_obj ON u_obj.imei = obj.imei
                JOIN gs_users us ON us.id = u_obj.user_id 
            WHERE
                us.id = 1646;
        """))

        for query in query_results:

            payload = [{
                "patente": str(query.patente),
                "latitude": float(query.latitude),
                "longitude": float(query.longitude),
                "datetime": query.date_time.strftime("%Y-%m-%d %H:%M:%S"),
                "speed": int(query.speed),
                "acc": True if query.acc == 1 else False,
                "empresa_proveedora_gps": 0
            }]

            url = "http://webservice.ctac.cl/location"

            payload = json.dumps(payload)
            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.json()["status"] == "OK":

                query_question_exist = """
                                        SELECT
                                            * 
                                        FROM
                                            integraciones_sinc 
                                        WHERE
                                            sinc_imei = :sinc_imei 
                                            AND sinc_dt_tracker = :sinc_dt_tracker;
                                    """
                
                query_exist = session.execute(text(query_question_exist), {
                    "sinc_imei": query.imei,
                    "sinc_dt_tracker": query.dt_tracker
                })

                if query_exist.rowcount == 0:

                    insert_integraciones_sinc({
                        "sinc_integ": load_data('INTEGRATION_NAME_TMS_1'),
                        "sinc_imei": query.imei,
                        "sinc_dt_tracker": query.dt_tracker,
                        "sinc_dt_server": query.dt_server,
                        "sinc_params": query.params,
                        "sinc_lat": query.latitude,
                        "sinc_lng": query.longitude,
                        "sinc_speed": query.speed,
                        "sinc_angle": query.angle,
                        "sinc_plate": query.patente,
                        "idpoint": 0
                    })

                print(f"punto enviado: {query.patente}")
            else:

                error_integracion = response.json()
                error_integracion["patente"] = query.patente
                print(error_integracion)
        
        return jsonify({"succes": True}), 200
    
    except Exception as e:
        return jsonify({"succes": False, "error": str(e)}), 500