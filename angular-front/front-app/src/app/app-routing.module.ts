import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { AuthorsComponent } from './authors/authors.component';
import { AuthorDetailsComponent } from './author-details/author-details.component';
import { BooksComponent } from './books/books.component';
import { BookDetailsComponent } from './book-details/book-details.component';

const routes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'authors', component: AuthorsComponent},
  {path: 'authors/:uuid', component: AuthorDetailsComponent},
  {path: 'books', component: BooksComponent},
  {path: 'books/:uuid', component: BookDetailsComponent},
  {path: '', redirectTo:'books', pathMatch:'full'},

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
