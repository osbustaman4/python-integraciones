from decouple import config as load_data
from datetime import datetime
from sqlalchemy import text, func

from lib.Stech import Stech

def insert_integraciones_sinc(data):
    try:
        session = Stech.get_session(load_data('ENVIRONMENTS'))

        query_insert = """
            INSERT INTO integraciones_sinc(
                sinc_integ
                ,sinc_imei
                ,sinc_dt_tracker
                ,sinc_dt_server
                ,sinc_params
                ,sinc_lat
                ,sinc_lng
                ,sinc_speed
                ,sinc_angle
                ,sinc_plate
                ,idpoint
            ) VALUES (
                :sinc_integ
                ,:sinc_imei
                ,:sinc_dt_tracker
                ,:sinc_dt_server
                ,:sinc_params
                ,:sinc_lat
                ,:sinc_lng
                ,:sinc_speed
                ,:sinc_angle
                ,:sinc_plate
                ,:idpoint
            ) ON DUPLICATE KEY UPDATE
                 sinc_integ = VALUES(sinc_integ),
                 sinc_imei = VALUES(sinc_imei),
                 sinc_dt_tracker = VALUES(sinc_dt_tracker),
                 sinc_dt_server = VALUES(sinc_dt_server),
                 sinc_params = VALUES(sinc_params),
                 sinc_lat = VALUES(sinc_lat),
                 sinc_lng = VALUES(sinc_lng),
                 sinc_speed = VALUES(sinc_speed),
                 sinc_angle = VALUES(sinc_angle),
                 sinc_plate = VALUES(sinc_plate),
                 idpoint = VALUES(idpoint)
        """

        session.execute(text(query_insert), data)
        session.commit()

    except Exception as e:
        print(str(e))
        return False
