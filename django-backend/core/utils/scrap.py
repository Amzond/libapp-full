

import requests
from author.models import Author
from book.models import Book
from bs4 import BeautifulSoup
from core.utils import elastic, exceptions


def scrap_books_from_vaga(url):
    
    obj_book_release_year = None
    obj_num_of_pages = None
    obj_isbn = ""
    obj_publisher = ""
    obj_cover = ""
    list_of_added_books = []
    
    if url:
        if 'vaga.lt' in url:
            vaga_url = url
    else:
        vaga_url = 'https://vaga.lt/naujos-knygos'   
    try:
        response = requests.get(vaga_url)
    except Exception:
        raise exceptions.ServiceUnavailable()
    
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
        if a_elements:
            obj_publisher = a_elements[0].text.strip()
        
        if a_elements and len(a_elements) >= 2:
            book_authors = a_elements[1].text
            authors = book_authors.split(',')

            for author in authors:
                author = author.strip()
                author_result = elastic.es_search_author_by_name(author)
                if author_result:
                    author_id = author_result
                else:
                    new_author = Author.objects.create(full_name=author)
                    author_id = new_author.id
                authors_list.append(author_id)
        
        
        if len(books_propery_des) >= 4:
             if books_propery_des[0].text.strip().isnumeric():
                obj_book_release_year = books_propery_des[0].text.strip()
            
        if len(books_propery_des) >= 4:
            obj_cover = books_propery_des[1].text.strip()
            
        if len(books_propery_des) >= 4:
            obj_isbn = books_propery_des[3].text.strip()
            
        if len(books_propery_des) >= 4:
            if books_propery_des[2].text.strip().isnumeric():
                obj_num_of_pages = books_propery_des[2].text.strip()
        
        obj = Book.objects.create(
            title=obj_book_title,
            num_of_pages=obj_num_of_pages,
            release_year=obj_book_release_year,
            isbn=obj_isbn,
            publisher = obj_publisher,
            cover = obj_cover
        )
        obj.authors.set(authors_list)
        
        
        list_of_added_books.append(obj_book_title)
    
    return list_of_added_books

def scrap_books_from_knygos(url):
    
    
    list_of_added_books = []
    if url:
        if 'knygos.lt' in url:
            knygos_url = url
    else:
        knygos_url = 'https://www.knygos.lt/lt/knygos/naujos/'
    try:
        response = requests.get(knygos_url)
    except Exception:
        raise exceptions.ServiceUnavailable()
    
    
    obj_book_release_year = None
    obj_num_of_pages = None
    obj_translator = ""
    obj_isbn = ""
    obj_language = ""
    obj_publisher = ""
    obj_cover = ""
    
    main_soup = BeautifulSoup(response.content, 'html.parser')
    
    book_links = main_soup.find_all('a', class_='product-link')
    for i, title in enumerate(book_links):
        
        book_url = title.get('href')
        book_url = book_url.strip()
        response = requests.get(book_url)
        soup = BeautifulSoup(response.content, 'html.parser')
 
        book_title = soup.find('h1').find('span', itemprop='name').text

        obj_book_title = book_title.strip()
        if elastic.es_search_book_by_title(obj_book_title):
            continue
        all_data = soup.find('ul', class_='about-product d-none d-md-block mt-4') 
        li_tag = all_data.find_all('li')
        authors_list = []
        for li in li_tag:
            
            if "Autorius:" in li.text:
                
                authors = li.text.replace('Autorius:', '').strip()
                authors_splited = authors.split(',')
                
                for author in authors_splited:
                    author = author.strip()
                author_result = elastic.es_search_author_by_name(author)
                if author_result:
                    author_id = author_result
                else:
                    new_author = Author.objects.create(full_name=author)
                    author_id = new_author.id
                authors_list.append(author_id)
                        
            if "Metai:" in li.text:
                obj_book_release_year = li.text.replace('Metai:', '').strip()
            if "Puslapiai:" in li.text:
                obj_num_of_pages = li.text.replace('Puslapiai:','').strip()
            if "Vertėjas:" in li.text:
                obj_translator = li.text.replace('Vertejas:', '').strip()
            if "ISBN:" in li.text:
                obj_isbn = li.text.replace('ISBN:', '').strip()
            if "Kalba:" in li.text:
                obj_language = li.text.replace('Kalba:', '').strip()
            if "Leidėjas:" in li.text:
                obj_publisher = li.text.replace('Leidėjas:', '').strip()
            if "Formatas:" in li.text:
                obj_cover = li.text.replace('Formatas:', '').strip()
         
              
        obj = Book.objects.create(
            title=obj_book_title,
            num_of_pages=obj_num_of_pages,
            release_year=obj_book_release_year,
            isbn=obj_isbn,
            translator=obj_translator,
            language=obj_language,
            publisher=obj_publisher,
            cover=obj_cover
        )
        obj.authors.set(authors_list)
        list_of_added_books.append(obj_book_title)
    
    return list_of_added_books


        
def scrap_single_book_from_vaga(url):
    list_of_added_books = []
    obj_book_release_year = None
    obj_num_of_pages = None
    obj_isbn = ""
    obj_publisher = ""
    obj_cover = ""
    if url:
        if 'vaga.lt' in url:
            vaga_url = url
    else:
        return "Bloga nuoroda" 
    try:
        response = requests.get(vaga_url)
    except Exception:
        raise exceptions.ServiceUnavailable()
    
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    obj_title = soup.find('div', class_='title-product')
    obj_title = obj_title.text.strip()
    
    if elastic.es_search_book_by_title(obj_title):
        return "tokia knyga jau yra"

    books_propery_des = soup.find_all('span', class_='propery-des')
    a_elements = soup.select('.brand a')
    
    authors_list = []
    if a_elements:
        obj_publisher = a_elements[0].text.strip()
        if a_elements and len(a_elements) >= 2:
            book_authors = a_elements[1].text
            authors = book_authors.split(',')

            for author in authors:
                author = author.strip()
                author_result = elastic.es_search_author_by_name(author)
                if author_result:
                    author_id = author_result
                else:
                    new_author = Author.objects.create(full_name=author)
                    author_id = new_author.id
                authors_list.append(author_id)
        
        if len(books_propery_des) >= 4:
            if books_propery_des[0].text.strip().isnumeric():
                obj_book_release_year = books_propery_des[0].text.strip()
        if len(books_propery_des) >= 4:
            obj_cover = books_propery_des[1].text.strip()
        if len(books_propery_des) >= 4:
            obj_isbn = books_propery_des[3].text.strip()
        if len(books_propery_des) >= 4:
            if books_propery_des[2].text.strip().isnumeric():
                obj_num_of_pages = books_propery_des[2].text.strip()
    
            
            
    obj = Book.objects.create(
        title=obj_title,
        num_of_pages=obj_num_of_pages,
        release_year=obj_book_release_year,
        isbn=obj_isbn,
        publisher = obj_publisher,
        cover = obj_cover
    )
    obj.authors.set(authors_list)
    list_of_added_books.append(obj_title)
    return list_of_added_books



def scrap_single_book_from_knygos(url):
    list_of_added_books = []
    if url:
        if 'knygos.lt' in url:
            knygos_url = url
    else:
        return "Bloga nuoroda"
    try:
        response = requests.get(knygos_url)
    except Exception:
        raise exceptions.ServiceUnavailable()
    obj_book_release_year = None
    obj_num_of_pages = None
    obj_translator = ""
    obj_isbn = ""
    obj_language = ""
    obj_publisher = ""
    obj_cover = ""
    
    soup = BeautifulSoup(response.content, 'html.parser')
    book_title = soup.find('h1').find('span', itemprop='name').text

    obj_book_title = book_title.strip()
    if elastic.es_search_book_by_title(obj_book_title):
        return "tokia knyga jau yra"
    all_data = soup.find('ul', class_='about-product d-none d-md-block mt-4') 
    li_tag = all_data.find_all('li')
    authors_list = []
    for li in li_tag:
            
        if "Autorius:" in li.text:
                
            authors = li.text.replace('Autorius:', '').strip()
            authors_splited = authors.split(',')
                
            for author in authors_splited:
                author = author.strip()
            author_result = elastic.es_search_author_by_name(author)
            if author_result:
                author_id = author_result
            else:
                new_author = Author.objects.create(full_name=author)
                author_id = new_author.id
            authors_list.append(author_id)
                        
        if "Metai:" in li.text:
            obj_book_release_year = li.text.replace('Metai:', '').strip()
        if "Puslapiai:" in li.text:
            obj_num_of_pages = li.text.replace('Puslapiai:','').strip()
        if "Vertėjas:" in li.text:
            obj_translator = li.text.replace('Vertejas:', '').strip()
        if "ISBN:" in li.text:
            obj_isbn = li.text.replace('ISBN:', '').strip()
        if "Kalba:" in li.text:
            obj_language = li.text.replace('Kalba:', '').strip()
        if "Leidėjas:" in li.text:
            obj_publisher = li.text.replace('Leidėjas:', '').strip()
        if "Formatas:" in li.text:
            obj_cover = li.text.replace('Formatas:', '').strip()
    
    obj = Book.objects.create(
        title=obj_book_title,
        num_of_pages=obj_num_of_pages,
        release_year=obj_book_release_year,
        isbn=obj_isbn,
        translator=obj_translator,
        language=obj_language,
        publisher=obj_publisher,
        cover=obj_cover
    )
    obj.authors.set(authors_list)
    list_of_added_books.append(obj_book_title)
    
    return list_of_added_books