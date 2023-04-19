import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, map } from 'rxjs/operators';
import { Observable, of } from 'rxjs';


const TOKEN_KEY = 'auth-token';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  url = 'http://127.0.0.1:8000/api/login/'
  constructor( private http: HttpClient) { }

  login(data: any): Observable<any>{

     return this.http.post<any>(this.url, data).pipe(
      map(response => {
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
        return data.username;
      }),
      catchError(error => {
        console.log(error);
        return error;
      })
    );
  }
  isLoggedIn(): boolean {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      return false;
    }
    const expiry = JSON.parse(atob(accessToken.split('.')[1])).exp;
    const isExpired = Date.now() > expiry * 1000;
    return !isExpired;
  }
  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
  public getToken(): string | null {
    const token = localStorage.getItem('access_token');
    return token
  }


}
