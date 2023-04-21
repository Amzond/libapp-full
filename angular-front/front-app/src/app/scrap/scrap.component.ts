import { Component } from '@angular/core';
import { ScrapService } from '../services/scrap.service';
import { LoginService } from '../services/login.service';


@Component({
  selector: 'app-scrap',
  templateUrl: './scrap.component.html',
  styleUrls: ['./scrap.component.scss']
})
export class ScrapComponent {
  isScannigVaga = false
  isScannigKnygos = false
  isAuthenticated = false
  url_vaga?: any
  url_knygos?: any
  booksVaga: any
  booksKnygos: any
  isVisibleVagaAddedBooks = false
  isVisibleKnygosAddedBooks = false
  VagaMessage = ''
  KnygosMessage = ''
  constructor(
    private loginService: LoginService,
    private scrapService: ScrapService,
  ){}

  ngOnInit(){
    this.isAuthenticated = this.loginService.isLoggedIn()
  }
  onVagaUrlSubmit(){
    this.isScannigVaga = true
    const bookStore = {
      'book_store': 'vaga',
      'url_vaga': this.url_vaga 
    }
    
    this.scrapService.scrapeDataVaga(bookStore).subscribe(
      response => {
        this.isScannigVaga = false
        if (response.added_books.length > 0){
          this.booksVaga = response.added_books
          this.isVisibleVagaAddedBooks = true
        }
        else{
          this.VagaMessage = "Nerasta naujų knygų"
        }
      },
      error => {
        this.VagaMessage = error
      }
    )
  }
  onVagaClick(){
    this.isScannigVaga = true
    const bookStore = {'book_store': 'vaga'};
    this.scrapService.scrapeDataVaga(bookStore).subscribe(
      response => {
        this.isScannigVaga = false
        if (response.added_books.length > 0){
          this.booksVaga = response.added_books
          this.isVisibleVagaAddedBooks = true
        }
        else{
          this.VagaMessage = "Nerasta naujų knygų"
        }
      },
      error => {
        this.VagaMessage = error
      }
    )
  }
  onKnygosUrlSubmit(){
    this.isScannigKnygos = true
    const bookStore = {
      'book_store': 'knygos',
      'url_knygos': this.url_knygos 
    }
    this.scrapService.scrapeDataVaga(bookStore).subscribe(
      response => {
        this.isScannigKnygos = false
        if (response.added_books.length > 0){
          this.booksKnygos = response.added_books
          this.isVisibleKnygosAddedBooks = true
        }
        else {
          this.KnygosMessage = "Nerasta naujų knygų"
        }
      },
      error => {
        this.KnygosMessage = error
      }
    )
  }
  onKnygosClick(){
    this.isScannigKnygos = true
    const bookStore = {'book_store': 'knygos'};
    
    this.scrapService.scrapeDataVaga(bookStore).subscribe(
      response => {
        this.isScannigKnygos = false
        if (response.added_books.length > 0){
          this.booksKnygos = response.added_books
          this.isVisibleKnygosAddedBooks = true
        }else{
          this.KnygosMessage = "Nerasta naujų knygų"
        }
      },
      error => {
        this.KnygosMessage = error
      }
    )
  }
}

