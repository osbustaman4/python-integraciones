import traceback
from decouple import config as load_data
from lib.Stech import Logger, Stech
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

class CronArauco():

    @classmethod
    def cron_arauco_01(self):
        try:
            session = Stech.get_session(load_data('ENVIRONMENTS'))
            query_search_overpass_data = """
                                        SELECT 
                                            gs_objects.imei
                                        FROM   gs_user_objects,
                                            gs_objects
                                        WHERE  gs_user_objects.user_id = 691
                                            AND gs_user_objects.imei = gs_objects.imei
                                            AND gs_objects.overpass = 0
                                        """
            
            response_search_overpass_data = session.execute(text(query_search_overpass_data)).fetchall()

            for data in response_search_overpass_data:
                query_update_overpass = text(f"UPDATE gs_objects SET overpass = 1 WHERE imei = :imei AND overpass = 0")
                session.execute(query_update_overpass, { 'imei': data[0] })
                session.commit()

            Logger.add_to_log("success", f"{len(response_search_overpass_data)} overpass actualizados", load_data('LOG_DIRECTORY'), "log_cron_arauco")
            return True

        except ValueError as ex:
            Logger.add_to_log("error", str(ex), load_data('LOG_DIRECTORY'), "log_cron_arauco")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_cron_arauco")
            return False

        except SQLAlchemyError as ex:
            Logger.add_to_log("error", str(ex), load_data('LOG_DIRECTORY'), "log_cron_arauco")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_cron_arauco")
            return False

        except Exception as ex:
            message = f"{str(ex)} - {str(traceback.format_exc())}"
            Logger.add_to_log("error", message, load_data('LOG_DIRECTORY'), "log_cron_arauco")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_cron_arauco")
            return False