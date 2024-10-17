from apscheduler.schedulers.background import BackgroundScheduler
from monitoring import monitor_products

# Функция для запуска планировщика задач
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(monitor_products, 'interval', hours=1)  # Обновляем цены каждый час
    scheduler.start()
    return scheduler
