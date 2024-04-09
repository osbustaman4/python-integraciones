import requests
from flask import request, jsonify, Blueprint

from lib.Stech import Logger, Stech, Validate
from decouple import config as load_data

from datetime import datetime
from sqlalchemy import text, func



main_funcion_ejemplo = Blueprint('main_funcion_ejemplo', __name__)
main_obt_ppu = Blueprint('main_obt_ppu', __name__)
main_send_data = Blueprint('main_send_data',__name__)



    

@main_obt_ppu.route('/', methods=['GET'])
def get_gps_data_and_send():
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
            DATE_SUB(obj.dt_tracker, INTERVAL {response_data_timezone[0]['timezone']}) AS date_time,
            obj.speed,
            ( CASE JSON_EXTRACT( obj.params, '$.io1' ) WHEN NULL THEN JSON_EXTRACT( obj.params, '$.io239' ) END ) AS acc,
            'stech' AS empresa_proveedora_gps
        FROM
            gs_objects obj
            JOIN gs_user_objects u_obj ON u_obj.imei = obj.imei
            JOIN gs_users us ON us.id = u_obj.user_id
        WHERE
	        us.id = 1646;
    
    """))

    response_data = [
        {
            "patente": result.patente,
            "latitude": result.latitude,
            "longitude": result.longitude,
            "date_time": result.date_time.isoformat(),  # Convertir el objeto de fecha y hora a formato ISO
            "speed": result.speed,
            "acc": result.acc,
            "empresa_proveedora_gps": result.empresa_proveedora_gps
        }
        for result in query_results
    ]

    # Llamar a la función enviar_datos y pasarle los datos obtenidos
    response_from_send_data = enviar_datos(response_data)
    
    return jsonify(response_from_send_data), 200

@main_send_data.route('/', methods=['POST'])
def enviar_datos():
    # Aquí se obtienen los datos necesarios
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
            DATE_SUB(obj.dt_tracker, INTERVAL {response_data_timezone[0]['timezone']}) AS date_time,
            obj.speed,
            ( CASE JSON_EXTRACT( obj.params, '$.io1' ) WHEN NULL THEN JSON_EXTRACT( obj.params, '$.io239' ) END ) AS acc,
            us.id AS empresa_proveedora_gps
        FROM
            gs_objects obj
            JOIN gs_user_objects u_obj ON u_obj.imei = obj.imei
            JOIN gs_users us ON us.id = u_obj.user_id
        WHERE
            obj.imei IN ( '65789024074843', '67688032817672' )
            AND us.username = 'admin'
        LIMIT 10
    """))

    response_data = [
        {
            "patente": result.patente,
            "latitude": result.latitude,
            "longitude": result.longitude,
            "date_time": result.date_time.isoformat(),  # Convertir el objeto de fecha y hora a formato ISO
            "speed": result.speed,
            "acc": result.acc,
            "empresa_proveedora_gps": result.empresa_proveedora_gps
        }
        for result in query_results
    ]

    url = 'http://webservice.ctac.cl/location'
    headers = {'Content-Type': 'application/json'}

    
    response = requests.post(url, json=response_data, headers=headers)

    if response.status_code == 200:
        return {'status': 'OK'}
    else:
        return {'status': 'Error', 'message': 'Hubo un error al enviar los datos al servicio.'}, 500