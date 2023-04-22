import { Injectable } from '@angular/core';
import { HttpClient } from  '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';


@Injectable({
  providedIn: 'root'
})
export class BooksService {

  constructor(
    private http: HttpClient,
    private authService: AuthService
    ) { }

  private url = 'http://127.0.0.1:8000/api/books';
  private search_url = 'http://127.0.0.1:8000/api/books/?full_text_search=';
  private filter_by_status_url = 'http://127.0.0.1:8000/api/books/?status=';


  // "genre__iexact="
  getBooks(): Observable<any> {
    return this.http.get<any>(this.url);
  }
  searchBooks(search?: any): Observable<any>{
    return this.http.get<any>(this.search_url+ search)
  }
  private authors_url = 'http://127.0.0.1:8000/api/authors'
  getAuthors(): Observable<any>{
    return this.http.get<any>(this.authors_url)
  }
  createBook(bookData: any): Observable<any>{
    const httpOptions = {
      headers: this.authService.getHeaders()
    };
    return this.http.post<any>(this.url+"/", bookData, httpOptions)
  }
  filterByStatus(status: string): Observable<any>{
    return this.http.get<any>(this.filter_by_status_url+status)
  }
  filterBooksByPages(from: string, to: string): Observable<any>{
    return this.http.get<any>(this.url+"/?num_of_pages__gte="+from+"&num_of_pages__lte="+to)
  }
  filterBooksByReleaseYear(from:any, to:any): Observable<any>{
    return this.http.get<any>(this.url+"/?release_year__gte="+from+"&release_year__lte="+to)
  }
  private get_genres_url = 'http://127.0.0.1:8000/api/get-all-genres/'
  getAllGenres(): Observable<any>{
    return this.http.get<any>(this.get_genres_url)
  }
  filterBooksByGenre(genre:any): Observable<any>{
    return this.http.get<any>(this.url+"/?genre__iexact="+genre)
  }
  private get_min_pages_url = 'http://127.0.0.1:8000/api/get-min-pages/'
  getMinPages(): Observable<any>{
    return this.http.get<any>(this.get_min_pages_url)
  }
  private get_max_pages_url = 'http://127.0.0.1:8000/api/get-max-pages/'
  getMaxPages(): Observable<any>{
    return this.http.get<any>(this.get_max_pages_url)
  }


}
