from core.celery import app
from django.core import management
from core.utils import scrap

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
    
@app.task(
    name='task.scrap.books.vaga.cb'
)
def task_scrap_books_vaga_cb():
    scrap.scrap_books_from_vaga('')
    
@app.task(
    name='task.scrap.books.knygos.cb'
)
def task_scrap_books_knygos_cb():
    scrap.scrap_books_from_knygos('')