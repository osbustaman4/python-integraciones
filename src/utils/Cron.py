import traceback

from src.Crones.CronArauco import CronArauco
from src.integrations.IntegrationTms import IntegrationTms

class Cron():

    @classmethod
    def integration_tms_01(self):
        try:
            IntegrationTms.integration_tms_01()
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())


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

