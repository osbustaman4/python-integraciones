import traceback

from src.Crones.CronArauco import CronArauco
from src.integrations.IntegrationTms import IntegrationTms
from src.integrations.IntegrationWaypoint import IntegrationWaypoint

class Integration():

    @classmethod
    def integration_tms_01(self):
        try:
            IntegrationTms.integration_tms_01()
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())

    @classmethod
    def integration_wp_01(self):
        try:
            IntegrationWaypoint.integration_wp_01()
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())


class Cron():


    @classmethod
    def cron_arauco_01(self):
        try:
            if CronArauco.cron_arauco_01():
                CronArauco.cron_arauco_01()
            elif not CronArauco.cron_arauco_01():
                print("No existe data para actualizar")
            
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())

