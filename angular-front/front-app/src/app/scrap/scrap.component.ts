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
  url_vaga_single_book?: any
  url_knygos?: any
  url_knygos_single_book?: any
  booksVaga: any
  booksKnygos: any
  isVisibleVagaAddedBooks = false
  isVisibleKnygosAddedBooks = false
  VagaMessage = ''
  KnygosMessage = ''
  scrapSingleBookErrorKnygos = ''
  scrapSingleBookErrorVaga = ''
  constructor(
    private loginService: LoginService,
    private scrapService: ScrapService,
  ){}

  ngOnInit(){
    this.isAuthenticated = this.loginService.isLoggedIn()
  }
  onVagaSingleUrlSubmit(){
    this.isScannigVaga = true
    const bookStore = {
      'book_store': 'vaga',
      'url': this.url_vaga_single_book 
    }
    this.scrapService.scrapeSingleBook(bookStore).subscribe(
      response =>{
        this.isScannigVaga = false

        if (response.added_books.length > 0){
          this.booksVaga = response.added_books
          this.isVisibleVagaAddedBooks = true
        }
        else{
          this.VagaMessage = "Nerasta naujų knygų"
        }
      },
      error =>{
        this.scrapSingleBookErrorVaga = "Įvyko klaida"
      }
    )

  }
  onKnygosSingleUrlSubmit(){
    this.isScannigKnygos = true
    const bookStore = {
      'book_store': 'knygos',
      'url': this.url_knygos_single_book 
    }
    this.scrapService.scrapeSingleBook(bookStore).subscribe(
      response =>{
        this.isScannigKnygos = false
        if (response.added_books.length > 0){
          this.booksKnygos = response.added_books
          this.isVisibleKnygosAddedBooks = true
        }
        else{
          this.KnygosMessage = "Nerasta naujų knygų"
        }
      },
      error =>{
        this.scrapSingleBookErrorKnygos = "Įvyko klaida"
      }
      )

  }
  onVagaUrlSubmit(){
    this.isScannigVaga = true
    const bookStore = {
      'book_store': 'vaga',
      'url': this.url_vaga 
    }
    
    this.scrapService.scrapeData(bookStore).subscribe(
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
        this.VagaMessage = "Įvyko klaida"
      }
    )
  }
  onVagaClick(){
    this.isScannigVaga = true
    const bookStore = {'book_store': 'vaga'};
    this.scrapService.scrapeData(bookStore).subscribe(
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
        this.VagaMessage = "Įvyko klaida"
      }
    )
  }
  onKnygosUrlSubmit(){
    this.isScannigKnygos = true
    const bookStore = {
      'book_store': 'knygos',
      'url': this.url_knygos 
    }
    this.scrapService.scrapeData(bookStore).subscribe(
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
        this.KnygosMessage = "Įvyko klaida"
      }
    )
  }
  onKnygosClick(){
    this.isScannigKnygos = true
    const bookStore = {'book_store': 'knygos'};
    
    this.scrapService.scrapeData(bookStore).subscribe(
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
        this.KnygosMessage = "Įvyko klaida"
      }
    )
  }
}

