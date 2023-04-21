import { Component } from '@angular/core';
import { BookDetailsService } from '../services/book-details.service';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-book-details',
  templateUrl: './book-details.component.html',
  styleUrls: ['./book-details.component.scss']
})
export class BookDetailsComponent {
  bookId: any;
  author: any;
  public books?: any;
  author_full_name?: any;
  authorsMap: any = {}; 
  editedBook: any = {};
  isEditVisible = false;
  isAuthenticated = false
  existingAuthors?: any;
  EditForm: FormGroup;
  errorMessage?: any;
  bookingVisibility = true;
  bookStatusCodes = [
    { value: '0', label: 'Nėra' },
    { value: '1', label: 'Užsakyta' },
    { value: '2', label: 'Yra' }
  ];
  constructor(
    private router: Router,
    private loginService: LoginService,
    private bookDetailsService : BookDetailsService, 
    private route: ActivatedRoute,
    private formBuilder: FormBuilder) {
      this.EditForm = this.formBuilder.group({
        title: ['', Validators.required],
        num_of_pages: [
          0,
          Validators.compose([
            Validators.min(0),
            Validators.pattern('^[0-9]+$')
          ])],
        release_year: [
          new Date().getFullYear(),
          Validators.compose([
            Validators.min(0),
            Validators.pattern('^[0-9]+$')
          ])],
        authors: [[]],
        genre: [''],
        status: ['0'],
        publisher: [''],
        rewards: [''],
        isbn: [''],
        language: [''],
        translator: [''],
        cover: ['']
      });
    }
  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.bookId = params.get('uuid');
    });
    this.bookDetailsService.getBookDetails(this.bookId).subscribe(
      book=> {
        this.books=book
        this.fetchAuthors()
        this.bookingVisibility = this.ifBooked()
      }
    )
    
    this.isAuthenticated = this.loginService.isLoggedIn()
  }
  fetchAuthors(): void {
    this.books.authors.forEach((authorId: string) => {
    this.bookDetailsService.getAuthorById(authorId).subscribe(
      auth => {
        this.author=auth
        this.authorsMap[authorId] = this.author;
      }); 
    });
  }
  getAuthorFullName(authorId: string): string{
    const author = this.authorsMap[authorId];
    return author ? author.full_name : '';
  }
  onDelete(id?: any){
    this.bookDetailsService.deleteBook(id).subscribe(
      response => {
        this.router.navigate(['books/']);
      },
      error =>{
        console.log("nepavyko istrint")
      }
    )
  }
  getExistingAuthors(){
    this.bookDetailsService.getAuthors().subscribe(
      author =>{
        this.existingAuthors=author})
  }
  onEdit(){
    this.getExistingAuthors()
    this.isEditVisible = true
    this.EditForm = this.formBuilder.group({
      title: [
        this.books.title, 
        Validators.required],
      num_of_pages: [
        this.books.num_of_pages, 
        Validators.compose([
          Validators.min(0),
          Validators.pattern('^[0-9]+$')
        ])],
      release_year: [
        this.books.release_year,          
        Validators.compose([
          Validators.min(0),
          Validators.pattern('^[0-9]+$')
        ])],
      authors: [
        this.books.authors],
      genre: [
        this.books.genre],
      status: [
        this.books.status],
      publisher: [
        this.books.publisher],
      rewards: [
        this.books.rewards],
      isbn: [
        this.books.isbn],
      language: [
        this.books.language],
      translator: [
        this.books.translator],
      cover: [
        this.books.cover]
    });
  }
  onEditSubmit(){
    this.bookDetailsService.editBook(this.books.id, this.EditForm.value).subscribe(
      response =>{
        location.reload();
      },
      error => {
        this.errorMessage = "Negalimas pavadinimas"
      }
    )
  }
  getStatusLabel(value: string): string {
    const statusCode = this.bookStatusCodes.find(status => status.value === value);
    return statusCode ? statusCode.label : 'Nežinomas statusas';
  }
  onBooking(){
    const data = {'id': this.bookId}
    this.bookDetailsService.bookBook(data).subscribe(
      response => {
        location.reload();
      },
      error =>{

      }
    )
  }
  ifBooked(): boolean{
    if (this.books.status !== '0'){
      return false
    }
    return true
  }
}

