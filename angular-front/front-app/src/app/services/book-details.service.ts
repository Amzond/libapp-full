import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { HttpClient } from  '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BookDetailsService {
  private url = 'http://127.0.0.1:8000/api/books/';
  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) { }


  getBookDetails(id?: string): Observable<any>{
    return this.http.get<any>(this.url+id)
  }
  private author_url = 'http://127.0.0.1:8000/api/authors';
  getAuthorById(id?: string): Observable<any>{
    return this.http.get<any>(this.author_url+"/"+id)
  }
  deleteBook(id?: string): Observable<any>{
    const httpOptions = {
      headers: this.authService.getHeaders()
    };
    return this.http.delete<any>(this.url+id, httpOptions);
  }
  getAuthors(): Observable<any>{
    return this.http.get<any>(this.author_url);
  }
  editBook(id?: any, data?:any): Observable<any>{
    const httpOptions = {
      headers: this.authService.getHeaders()
    };
    return this.http.patch<any>(this.url+id, data, httpOptions);
  }
}
