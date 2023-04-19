import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { HttpClient } from  '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class AuthorService {

  constructor(
    private http: HttpClient,
    private authService: AuthService) { }

  private url = 'http://127.0.0.1:8000/api/authors';
  private search_url = 'http://127.0.0.1:8000/api/authors/?full_text_search=';

  getAuthors(): Observable<any> {
    return this.http.get<any>(this.url);
  }
  searchAuthors(search?: string): Observable<any>{
    return this.http.get<any>(this.search_url + search)
  }
  createAuthor(authorData: any): Observable<any>{
    const httpOptions = {
      headers: this.authService.getHeaders()
    };
    return this.http.post<any>(this.url+"/", authorData, httpOptions)
  }
}
