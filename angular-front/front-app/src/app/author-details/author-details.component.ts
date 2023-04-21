import { Component } from '@angular/core';
import { AuthorDetailsService } from '../services/author-details.service';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-author-details',
  templateUrl: './author-details.component.html',
  styleUrls: ['./author-details.component.scss']
})
export class AuthorDetailsComponent {
  AuthorId: any;
  authorDetails?: any;
  message?: any;
  isAuthenticated?: any;
  EditFormVisible = false
  editErrorMsg?: any;
  emailInput?: any;
  constructor(
    private authorDetailsService: AuthorDetailsService, 
    private route: ActivatedRoute,
    private router: Router,
    private loginService: LoginService,
    private formBuilder: FormBuilder){
      this.EditForm = this.formBuilder.group({
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
  EditForm: FormGroup;
  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.AuthorId = params.get('uuid');
      
      this.authorDetailsService.getAuthorDetails(this.AuthorId).subscribe(
        author =>{
          this.authorDetails = author
        }
      )
    });
    this.isAuthenticated = this.loginService.isLoggedIn()
  }
  onDelete(id?: any): void{
    this.authorDetailsService.deleteAuthor(id).subscribe(
      response => {
        this.router.navigate(['authors/']);
      },
      error =>{
        this.message = "Negalima ištrinti autoriaus nes jis yra priskirtas prie knygos/ų";
      }
    )
  }
  onEdit(){
    this.EditFormVisible = true
    this.EditForm = this.formBuilder.group({
      full_name: [
        this.authorDetails.full_name, 
        Validators.required
      ],
      email: [
        this.authorDetails.email,[
        Validators.email, 
        Validators.maxLength(50)]
      ],
      phone: [
        this.authorDetails.phone, 
        Validators.compose([Validators.pattern('^[0-9]+$'), 
        Validators.maxLength(16)])
      ],
      born: [
        this.authorDetails.born,
        Validators.compose([
          Validators.min(0),
          Validators.pattern('^[0-9]+$')
        ])],
      rewards: [
        this.authorDetails.rewards
      ],
      country: [
          this.authorDetails.country
      ],
      number_of_books: [
        this.authorDetails.number_of_books,
        Validators.compose([
          Validators.min(0),
          Validators.pattern('^[0-9]+$')
        ])
      ]
    });
  }
  onEditSubmit(){
    this.authorDetailsService.editAuthor(this.authorDetails.id, this.EditForm.value).subscribe(
      response => {
        location.reload();
      },
      error => {
        this.editErrorMsg = "Toks autorius jau egzistuoja"
      }
    )
  }
}
