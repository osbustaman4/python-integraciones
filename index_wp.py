from app_config import configure
from src import init_app
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from src.utils.Cron import Cron, Integration

configuration = configure['development']
app = init_app(configuration)

# Agregar esta línea para definir la variable 'application'
application = app

task_003 = BackgroundScheduler()
task_003.add_job(Integration.integration_wp_01, 'interval', seconds=10) 
task_003.start()


if __name__ == '__main__':
    #load_dotenv()
    app.run(host='0.0.0.0', port=5300)
    # app.run(host='192.168.100.16', port=5000)
