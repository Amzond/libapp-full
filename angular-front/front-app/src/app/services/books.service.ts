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

}
