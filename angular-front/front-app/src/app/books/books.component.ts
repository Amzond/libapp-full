import { Component} from '@angular/core';
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
  selectedStatus: string = '';
  selectedGenre: string = '';
  newBookForm: FormGroup;
  searchTerm: string = '';
  isAuthenticated = false
  fromValue = '0';
  toValue = '2500';
  fromYearValue = '0';
  allGenres: any;
  fromPagesMin = '0'
  toPagesMax = '2500'
  searchError = ''
  filterByYearsError = ''
  toYearValue = new Date().getFullYear();
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
      title: ['', 
        Validators.required,
        Validators.maxLength(254)
      ],
      num_of_pages: [
        0, 
        Validators.min(0)
      ],
      release_year: [
        new Date().getFullYear(),
        Validators.compose([
          Validators.min(0),
          Validators.pattern('^[0-9]+$')
        ])
      ],
      authors: [[],
        Validators.required
      ],
      genre: ['',
        Validators.maxLength(254)
      ],
      status: ['0'],
      publisher: ['',
        Validators.maxLength(50)
      ],
      rewards: ['',
        Validators.maxLength(100)
      ],
      isbn: ['',
        Validators.maxLength(16)
      ],
      language: ['',
        Validators.maxLength(50)
      ],
      translator: ['',
        Validators.maxLength(50)
      ],
      cover: ['',
        Validators.maxLength(50)
      ]
    });
   }
   posts : any;
   public books?: any;
   public bookDetails?: any;
   showBookForm = false
   existingAuthors?: any;
   bookAuthors?: any;
   errorMsg = ''
   errorMessage?: any;
   sortOrder = "desc"
   orderMsg = "A...Z"

   ngOnInit() {
      this.getBooksData()
      this.getAllGenres()
      this.getMinPageNum()
      this.getMaxPageNum()
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
      },
      error => {
        this.searchError = "Įvyko klaida"
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
      title: [
        '', 
        Validators.required,
        Validators.maxLength(254),
      ],
      num_of_pages: [0, 
        Validators.min(0)
      ],
      release_year: [
        new Date().getFullYear(),
        Validators.compose([
          Validators.min(0),
          Validators.pattern('^[0-9]+$')
        ])],
      authors: [[],
        Validators.required
      ],
      genre: [''],
      status: ['0'],
      publisher: ['',
        Validators.maxLength(50)
      ],
      rewards: ['',
        Validators.maxLength(100)
      ],
      isbn: ['',
        Validators.maxLength(16)
      ],
      language: ['',
        Validators.maxLength(50)
      ],
      translator: ['',
        Validators.maxLength(50)
      ],
      cover: ['',
        Validators.maxLength(50)
      ]
    });
  }
  onSubmitCreateBook(){
    const bookData = this.newBookForm.value;
    if (!Array.isArray(bookData.authors) || bookData.authors.length === 0){
      this.errorMessage = "Autorius privalomas" 
    }else{
      this.booksService.createBook(bookData).subscribe(
      response=>{
        location.reload();
      },
      error => {
        this.errorMessage = "Tokia knyga jau egzistuoja"
      }
    )
    }
  }
  getStatusLabel(value: string): string {
      const statusCode = this.bookStatusCodes.find(status => status.value === value);
      if (statusCode) {
        return statusCode.label;
      } else {
        return 'Nežinomas statusas';
      }
    }
  getStatusClass(status: string) {
    switch(status) {
      case '2':
        return 'green-background';
      case '1':
        return 'yellow-background';
      case '0':
        return 'red-background';
      default:
        return 'grid-item';
    }
  }

  getExistingAuthors(){
    this.booksService.getAuthors().subscribe(
      author =>{
        this.existingAuthors = author
      },
      error => {
        this.existingAuthors = []
      }
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
  onScrapMenu(){
    this.router.navigate(['/scrap'])
  }
  onSelectStatus( status: string) {
      this.booksService.filterByStatus(status).subscribe(
        book =>{
          this.books = book
        }
      )
  }
  onSelectPages(from: any, to:any){
    if(from){
      this.fromValue = from.target.value
    }
    if(to){
      this.toValue = to.target.value
    }
    this.booksService.filterBooksByPages(this.fromValue,this.toValue).subscribe(
      book =>{
        this.books = book
      }
    )
  }
  onSelectReleaseYears(from: any, to:any){
    if(from){
      this.fromYearValue = from.target.value
    }
    if(to){
      this.toYearValue = to.target.value
    }
    this.booksService.filterBooksByReleaseYear(this.fromYearValue, this.toYearValue).subscribe(
      book =>{
        this.books = book
      },
      error =>{
        this.filterByYearsError = "Įvyko klaida"
      }
    )
  }
  getAllGenres(){
    this.booksService.getAllGenres().subscribe(
      genre =>{
        this.allGenres = genre
      }
    )
  }
  onGenres(value:any){
    
    this.booksService.filterBooksByGenre(value).subscribe(
      book => {
        this.books = book
      }
    )
  }
  getMaxPageNum(){
    this.booksService.getMaxPages().subscribe(
      response => {
        this.toPagesMax = response
      },
      error =>{
        this.toPagesMax = '2500'
      }
    )
  }
  getMinPageNum(){
    this.booksService.getMinPages().subscribe(
      respones => {
        this.fromPagesMin = respones
      },
      error =>{
        this.fromPagesMin = '0'
      }
    )
  }

}
