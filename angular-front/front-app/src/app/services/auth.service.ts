import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { LoginService } from './login.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private loginService: LoginService) { }

  public getHeaders(): HttpHeaders {
    const token = this.loginService.getToken();
    return new HttpHeaders({ 'Authorization': `Bearer ${token}` });
  }
}
