import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LoginService } from '../services/login.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  username?: string;
  password?: string;
  isLoggedIn?: boolean;

  errorMessage?: any ;
  constructor(
    private router: Router,
    private loginService: LoginService,
    ) { }

  ngOnInit(){
    this.isLoggedIn = this.loginService.isLoggedIn()
  }

  onLogin(): void {
    const data = {
      username: this.username,
      password: this.password
    };
    this.loginService.login(data).subscribe(
      success => {
        if (success) {
          console.log('Login successful');
          this.router.navigate(['']);
        } else {
          console.log('Login failed');
          this.errorMessage = "Blogas prisijungimo vardas arba slaptažodis"
        }
      },
      error => {
        console.log('Login error:', error);
        this.errorMessage = "Blogas prisijungimo vardas arba slaptažodis"
      }
    );
  }
  onLogout(): void {
    this.loginService.logout()
    location.reload()
  }
  
}
