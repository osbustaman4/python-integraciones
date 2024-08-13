import json
import requests
import traceback
from decouple import config as load_data
from lib.Stech import Logger, Stech
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from src.utils.Utils import insert_integraciones_sinc, update_integraciones_sinc

class IntegrationWaypoint():

    @classmethod
    def integration_wp_01(self):
        try:
            session = Stech.get_session(load_data('ENVIRONMENTS'))

            result_time_zone = session.execute(text("""SELECT timezone FROM gs_users WHERE id = 1;"""))

            response_data_timezone = [
                {
                    "timezone": result.timezone,
                }
                for result in result_time_zone
            ]

            data_timezone = response_data_timezone[0]["timezone"]
            if "hour" in data_timezone.lower():
                data_timezone = data_timezone.replace("hour", "HOUR")

            # Inserta el valor de la zona horaria directamente en la cadena de consulta
            query_string = f"""
                SELECT
                    UNIX_TIMESTAMP(DATE_SUB(obj.dt_tracker, INTERVAL {data_timezone})) AS fecha,
                    obj.lat AS latitud,
                    obj.lng AS longitud,
                    obj.altitude AS altitud,
                    obj.angle AS cog,
                    obj.speed AS velocidad,
                    obj.satelites AS nsat,
                    obj.plate_number AS patente,
                    obj.imei,
                    obj.dt_server,
                    DATE_SUB(obj.dt_tracker, INTERVAL -4 HOUR) AS fecha_tracker,
                    obj.angle,
                    obj.params

                FROM
                    gs_objects obj
                    JOIN gs_user_objects u_obj ON u_obj.imei = obj.imei
                    JOIN gs_users us ON us.id = u_obj.user_id 
                WHERE
                    us.id = 1743;
            """

            # Ejecuta la consulta
            query_results = session.execute(text(query_string)).fetchall()

            for query in query_results:

                payload = [
                            {
                                "fecha": query.fecha,
                                "latitud": query.latitud,
                                "longitud": query.longitud,
                                "altitud": query.altitud,
                                "velocidad": query.velocidad,
                                "cog": query.cog,
                                "nsat": query.nsat,
                                "realtime": True,
                                "input": [
                                    0,
                                    0,
                                    0,
                                    0
                                ],
                                "hdop": 0.0,
                                "ignicion": 0,
                                "adc": [
                                    -200.0,
                                    -200.0,
                                    -200.0,
                                    -200.0
                                ],
                                "power": 0,
                                "horometro": 0,
                                "odometro": 0,
                                "panico": 0,
                                "bateria": 0.0,
                                "bateriaInt": 0.0,
                                "patente": query.patente,
                                "tercerojo": 0,
                                "aceleracion": 0,
                                "frenada": 0,
                                "giro": 0
                            }
                    ]

                url = "https://api.waypoint.cl/inbound/inboundLD"

                payload = json.dumps(payload)
                headers = {
                    'Content-Type': 'application/json',
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                if response.status_code == 200:

                    code_response = response.json()
                    if code_response["code"] == 0:

                        query_question_exist = """
                                                SELECT
                                                    * 
                                                FROM
                                                    integraciones_sinc 
                                                WHERE
                                                    sinc_imei = :sinc_imei;
                                            """
                        
                        query_exist = session.execute(text(query_question_exist), {
                            "sinc_imei": query.imei
                        })

                        data_integraciones_sinc = {
                            "sinc_integ": load_data('INTEGRATION_NAME_WP_1'),
                            "sinc_imei": query.imei,
                            "sinc_dt_tracker": query.fecha_tracker,
                            "sinc_dt_server": query.dt_server,
                            "sinc_params": query.params,
                            "sinc_lat": query.latitud,
                            "sinc_lng": query.longitud,
                            "sinc_speed": query.velocidad,
                            "sinc_angle": query.angle,
                            "sinc_plate": query.patente,
                            "idpoint": 0
                        }

                        if query_exist.rowcount == 0:
                            insert_integraciones_sinc(data_integraciones_sinc)
                            Logger.add_to_log("success", f"insert: {query.patente}", load_data('LOG_DIRECTORY'), "log_waypoint")

                        else:
                            update_integraciones_sinc(data_integraciones_sinc)
                            Logger.add_to_log("success", f"update: {query.patente}", load_data('LOG_DIRECTORY'), "log_waypoint")

                        Logger.add_to_log("success", f"punto enviado: {query.patente}", load_data('LOG_DIRECTORY'), "log_waypoint")
                else:

                    error_integracion = response.json()
                    error_integracion["patente"] = query.patente
                    Logger.add_to_log("error", error_integracion, load_data('LOG_DIRECTORY'), "log_waypoint")
                    Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_waypoint")
        
        except SQLAlchemyError as ex:
            Logger.add_to_log("error", str(ex), load_data('LOG_DIRECTORY'), "log_waypoint")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_waypoint")

        except Exception as ex:
            Logger.add_to_log("error", str(ex), load_data('LOG_DIRECTORY'), "log_waypoint")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_waypoint")
