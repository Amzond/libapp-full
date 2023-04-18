from author.models import Author
from celery.utils.log import get_task_logger
from core.celery import app
from django.core import management

logger = get_task_logger(__name__)

@app.task(
    name='task.author.delete'
)
def task_author_delete(author_ids: list) -> None:
    try:
        authors = Author.objects.prefetch_related('book_set').filter(pk__in=author_ids)
        for author in authors:
            if not author.book_set.exists():
                author.delete()
    except ValueError:
        logger.info(
            'task delete author failed',
            extra={'author_ids': author_ids}
        )
        
@app.task(
    name='task.author.sycn.elastic.cb'
)
def task_author_sync_elastic_cb():
    management.call_command('search_index',
                            '--populate',
                            '--models',
                            'author',
                            '-f'
                            )