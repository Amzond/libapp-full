from author.models import Author
from django.conf import settings
from elasticsearch import Elasticsearch


def init_elastic()-> Elasticsearch:
    return Elasticsearch(settings.ELASTIC_HOST)

def es_search_book_by_title(book_title: str):
    es = init_elastic()
    flag = True
    try:
        response = es.search(index=settings.ELASTIC_BOOK_INDEX, body=es_search_book_by_title_query(book_title), _source=False)
        id = [result['_id'] for result in response['hits']['hits']]
        if not id:
            flag = False
    except Exception:
        pass
    return flag

def es_search_author_by_name(author_name: str):
    es = init_elastic()
    try:
        response = es.search(index=settings.ELASTIC_AUTHOR_INDEX, body=es_search_author_by_name_query(author_name))
        id = [result['_id'] for result in response['hits']['hits']]
        if not id:
            return None
    except Exception:
        pass
    return id[0]


def es_full_text_search_query(value: str)-> dict:
    return {
        'query':{
            'multi_match':{
                'query': value
            }
        }
    }
    
def es_search_book_by_title_query(value: str)->dict:
    return {
        "query": {
            "match": {
                "title.keyword": value
            }
        }
    }
def es_search_author_by_name_query(value: str)->dict:
    return {
        "query": {
            "match": {
                "full_name.keyword": value
            }
        }
    }
    
