import { Component } from '@angular/core';
import { AuthorService } from '../services/author.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginService } from '../services/login.service';
import { sortBy } from 'lodash';

@Component({
  selector: 'app-authors',
  templateUrl: './authors.component.html',
  styleUrls: ['./authors.component.scss']
})
export class AuthorsComponent {
  
  authors?: any;
  searchTerm: string = '';
  isFormVisible = false;
  isAuthenticated = false
  errorMessage?: any;
  sortOrder = "desc"
  orderMsg = "A...Z"

  constructor(
    private aurhorService: AuthorService, 
    private router: Router,
    private loginService: LoginService,
    private formBuilder: FormBuilder){
      this.authorForm = this.formBuilder.group({
        full_name: ['', Validators.required],
        email: ['', [
          Validators.email, 
          Validators.maxLength(50)]],
        phone: ['', 
          Validators.compose([Validators.pattern('^[0-9]+$'), 
          Validators.maxLength(16)])],
        born: [null,
          Validators.compose([
            Validators.min(0),
            Validators.pattern('^[0-9]+$')
          ])],
        rewards: [''],
        country: [''],
        number_of_books: [null,
          Validators.compose([
            Validators.min(0),
            Validators.pattern('^[0-9]+$')
          ])]
        });
  }
  authorForm: FormGroup;

  ngOnInit() {
    this.getAuthors()
    this.isAuthenticated = this.loginService.isLoggedIn()
  }
  private getAuthors(): void{
    this.aurhorService.getAuthors().subscribe(
      (author)=>{
        this.authors=author
        this.authors = this.authors.sort((
          a: { full_name: any; },
          b: { full_name: any; }) => a.full_name.localeCompare(b.full_name))
      }
    )
  }
  onSearch(){
    this.aurhorService.searchAuthors(this.searchTerm).subscribe(
      (author)=>{
        this.authors=author
      }
      )
  }
  showForm(){
    this.isFormVisible = true;
    this.authorForm = this.formBuilder.group({
      full_name: ['', Validators.required],
      email: ['', [
        Validators.email, 
        Validators.maxLength(50)]],
      phone: ['', 
        Validators.compose([Validators.pattern('^[0-9]+$'), 
        Validators.maxLength(16)])],
      born: [null,
        Validators.compose([
          Validators.min(0),
          Validators.pattern('^[0-9]+$')
        ])],
      rewards: [''],
      country: [''],
      number_of_books: [null,
        Validators.compose([
          Validators.min(0),
          Validators.pattern('^[0-9]+$')
          ])]
      });
  }
  onCreateAuthor() {
    const authorData = this.authorForm.value;
    this.aurhorService.createAuthor(authorData).subscribe(
      response=>{
          location.reload();
      },
      error => {
        this.errorMessage = "Toks autorius jau yra" 
      }
    )
  }
  onAuthor(id?: any){
    this.router.navigate(['/authors', id]);
  }
  toggleSortOrder() {
    if (this.sortOrder === 'asc') {
      this.authors = this.authors.sort((
        a: { full_name: any; },
        b: { full_name: any; }) => a.full_name.localeCompare(b.full_name))
      this.sortOrder = 'desc';
      this.orderMsg = 'A...Z';
    } else {
      this.authors = this.authors.sort((
        a: { full_name: any; },
        b: { full_name: any; }) => b.full_name.localeCompare(a.full_name))

      this.sortOrder = 'asc';
      this.orderMsg = 'Z...A';
    }
  }
  buttonStyle(button : HTMLButtonElement) {
    button.style.backgroundColor = 'blue';
  }
  buttonStyleHover(button: HTMLButtonElement) {
    button.style.backgroundColor = 'blue';
  }
}




