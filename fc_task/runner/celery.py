from celery import Celery
from fc_task.config import load_redis_url

redis_url = load_redis_url()

app = Celery(
    "fc_task",
    broker=redis_url,
    backend=redis_url,
    include=["fc_task.runner.tasks"],
)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
