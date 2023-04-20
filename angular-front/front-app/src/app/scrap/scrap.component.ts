import { Component } from '@angular/core';
import { ScrapService } from '../services/scrap.service';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-scrap',
  templateUrl: './scrap.component.html',
  styleUrls: ['./scrap.component.scss']
})
export class ScrapComponent {

  isAuthenticated = false

  constructor(
    private loginService: LoginService,
    private scrapService: ScrapService,
  ){}

  ngOnInit(){
    this.isAuthenticated = this.loginService.isLoggedIn()
  }
  onVagaClick(){
    const bookStore = {'book_store': 'vaga'};

    this.scrapService.scrapeDataVaga(bookStore).subscribe(
      response => {
        console.log(response)
      },
      error => {
        console.log(error)
      }
    )
  }
  onKnygosClick(){
    const bookStore = {'book_store': 'knygos'};

    this.scrapService.scrapeDataVaga(bookStore).subscribe(
      response => {
        console.log(response)
      },
      error => {
        console.log(error)
      }
    )
  }
}

