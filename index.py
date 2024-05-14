from app_config import configure
from src import init_app
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from src.utils.Cron import Cron

configuration = configure['development']
app = init_app(configuration)

# Agregar esta línea para definir la variable 'application'
application = app

task_001 = BackgroundScheduler()
task_001.add_job(Cron.integration_tms_01, 'interval', seconds=10) 
task_001.start()

task_002 = BackgroundScheduler()
task_002.add_job(Cron.cron_arauco_01, 'interval', hours=1) 
task_002.start()


if __name__ == '__main__':
    #load_dotenv()
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='192.168.100.16', port=5000)
