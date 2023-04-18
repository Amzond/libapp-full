from core.celery import app
from django.core import management


@app.task(
    name='task.book.sync.elastic.cb'
)
def task_book_sync_elastic_cb():
    management.call_command('search_index',
                            '--populate',
                            '--models',
                            'book',
                            '-f'
                            )