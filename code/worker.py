import os
from time import sleep
from celery import Celery, current_task
from celery.bin import worker
from .item import Item

app = Celery(
    "worker",
    broker="amqp://okteto:okteto@rabbitmq:5672//"
)
app.conf.task_routes = {
    "app.worker.celery_worker.queue": "items"}

app.conf.update(task_track_started=True)

@app.task(acks_late=True)
def process_item(id: int,quantity: int, price: float) -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': i*10})
    return f"finished processing item: {id} | {quantity} | {price}"