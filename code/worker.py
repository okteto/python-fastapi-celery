import os
from time import sleep
from celery import Celery, current_task
from celery.bin import worker
from item import Item

celery_app = Celery(
    "worker",
    broker="amqp://okteto:okteto@rabbitmq:5672//"
)
celery_app.conf.task_routes = {
    "app.worker.celery_worker.queue": "items"}

celery_app.conf.update(task_track_started=True)

@celery_app.task(acks_late=True)
def process_item(id: int,quantity: int, price: float) -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': i*10})
    return f"processed item: {id} | {quantity} | {price}"

if __name__ == '__main__':
    worker = worker.worker(app=celery_app)
    options = {
        'loglevel': 'INFO',
        'traceback': True,
    }

    worker.run(**options)