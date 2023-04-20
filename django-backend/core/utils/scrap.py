import requests
from author.models import Author
from book.models import Book
from bs4 import BeautifulSoup
from core.utils import elastic


def scrap_books_from_vaga():
    
    vaga_url = 'https://vaga.lt/naujos-knygos'  
    response = requests.get(vaga_url)

    main_soup = BeautifulSoup(response.content, 'html.parser')
        
    book_titles = main_soup.find_all('p', class_='name')
    for i, title in enumerate(book_titles):
        striped_title = title.text.strip()
        if elastic.es_search_book_by_title(striped_title):
            continue
        
        book_url = title.find('a').get('href')
        response = requests.get(book_url)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        books_propery_des = soup.find_all('span', class_='propery-des')
        a_elements = soup.select('.brand a')
        
        obj_book_title = title.text.strip()
        authors_list = []
        if a_elements and len(a_elements) >= 2:
            book_authors = a_elements[1].text
            authors = book_authors.split(',')
            # authors_list = [elastic.es_search_author_by_name(author) or Author.objects.create(full_name=author).id for author in authors if author.strip()]

            for author in authors:
                author = author.strip()
                author_result = elastic.es_search_author_by_name(author)
                if author_result:
                    author_id = author_result.id
                else:
                    new_author = Author.objects.create(full_name=author)
                    author_id = new_author.id
                authors_list.append(author_id)
 
        #obj_book_release_year = books_propery_des[0].text.strip() if len(books_propery_des) >= 3 else ''
        if len(books_propery_des) >= 3:
            obj_book_release_year = books_propery_des[0].text.strip()
            
        #obj_num_of_pages = books_propery_des[2].text.strip() if len(books_propery_des) >= 3 else ''
        if len(books_propery_des) >= 3:
            obj_num_of_pages = books_propery_des[2].text.strip()
        
        obj = Book.objects.create(
            title=obj_book_title,
            num_of_pages=obj_num_of_pages,
            release_year=obj_book_release_year
        )
        obj.authors.set(authors_list)
        

def scrap_books_from_knygos():
    
    knygos_url = 'https://www.knygos.lt/lt/knygos/naujos/'
    response = requests.get(knygos_url)

    main_soup = BeautifulSoup(response.content, 'html.parser')
    
    book_links = main_soup.find_all('a', class_='product-link')
    for i, title in enumerate(book_links):
        
        book_url = title.get('href')
        book_url = book_url.strip()
        response = requests.get(book_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        import ipdb
        ipdb.set_trace()
        book_title = soup.find('h1')
        stripet_book_title = book_title.strip()
        if elastic.es_search_book_by_title(stripet_book_title):
            continue
