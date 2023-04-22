import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { HttpClient } from  '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthorDetailsService {

  private url = 'http://127.0.0.1:8000/api/authors/';

  constructor(
    private http: HttpClient,
    private authService: AuthService) { }

  getAuthorDetails(id?: string): Observable<any>{
    return this.http.get<any>(this.url+id)
  }

  deleteAuthor(id?: string): Observable<any>{
    const httpOptions = {
      headers: this.authService.getHeaders()
    };
    return this.http.delete<any>(this.url+id, httpOptions);
  }

  editAuthor(id?: any, data?: any): Observable<any>{
    const httpOptions = {
      headers: this.authService.getHeaders()
    };
    return this.http.patch<any>(this.url+id, data, httpOptions);
  } 
  private url_get_books = 'http://127.0.0.1:8000/api/get-author-books/'
  getAuthorBooks(id: any): Observable<any>{
    return this.http.post<any>(this.url_get_books, id)
  }
}

