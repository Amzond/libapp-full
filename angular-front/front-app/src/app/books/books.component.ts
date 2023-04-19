import { Component } from '@angular/core';
import { BooksService } from '../services/books.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginService } from '../services/login.service';
import { sortBy } from 'lodash';
@Component({
  selector: 'app-books',
  templateUrl: './books.component.html',
  styleUrls: ['./books.component.scss']
})
export class BooksComponent {
  newBookForm: FormGroup;
  searchTerm: string = '';
  isAuthenticated = false
  bookStatusCodes = [
    { value: '0', label: 'Nėra' },
    { value: '1', label: 'Užsakyta' },
    { value: '2', label: 'Yra' }
  ];
  constructor( 
    private booksService: BooksService, 
    private router: Router,
    private loginService: LoginService, 
    private formBuilder: FormBuilder) {
    this.newBookForm = this.formBuilder.group({
      title: ['', Validators.required],
      num_of_pages: [0, Validators.min(0)],
      release_year: [new Date().getFullYear()],
      authors: [[]],
      genre: [''],
      status: ['0']
    });
   }
   posts : any;
   public books?: any;
   public bookDetails?: any;
   showBookForm = false
   existingAuthors?: any;
   bookAuthors?: any;
   errorMsg?: any;
   errorMessage?: any;
   sortOrder = "desc"
   orderMsg = "A...Z"

   ngOnInit() {
      this.getBooksData()
      this.isAuthenticated = this.loginService.isLoggedIn()
   }
    getBooksData(){
      this.booksService.getBooks().subscribe(
        book => {
          this.books = book
          this.books = this.books.sort((
            a: { title: any; },
            b: { title: any; }) => a.title.localeCompare(b.title))
        },
        error => {
          this.errorMsg = "Atsiprašome paslauga laikinai nepasiekiama"
        }
      )
   }
  onSearch(){
    this.booksService.searchBooks(this.searchTerm).subscribe(
      book => {
        this.books = book
      }
    )
   }
  onBook(id?: any){
    this.router.navigate(['/books', id])  
  }
  onCreate(){
    this.getExistingAuthors()
    this.showBookForm=true
    this.newBookForm = this.formBuilder.group({
      title: ['', Validators.required],
      num_of_pages: [0, Validators.min(0)],
      release_year: [new Date().getFullYear()],
      authors: [[]],
      genre: [''],
      status: ['0']
    });

   }
  onSubmitCreateBook(){
    const bookData = this.newBookForm.value;
    this.booksService.createBook(bookData).subscribe(
      response=>{
        location.reload();
      },
      error => {
        this.errorMessage = "Tokia knyga jau egzistuoja"
      }
    )
   }
  getStatusLabel(value: string): string {
      const statusCode = this.bookStatusCodes.find(status => status.value === value);
      return statusCode ? statusCode.label : 'Nežinomas statusas';
    }
  getExistingAuthors(){
    this.booksService.getAuthors().subscribe(
      author =>{
        this.existingAuthors = author
      },
      error => {}
    )
  }

  toggleSortOrder() {
    if (this.sortOrder === 'asc') {
      this.books = this.books.sort((
        a: { title: any; },
        b: { title: any; }) => a.title.localeCompare(b.title))
      this.sortOrder = 'desc';
      this.orderMsg = 'A...Z';
    } else {
      this.books = this.books.sort((
        a: { title: any; },
        b: { title: any; }) => b.title.localeCompare(a.title))
      this.sortOrder = 'asc';
      this.orderMsg = 'Z...A';
    }
  }

}
