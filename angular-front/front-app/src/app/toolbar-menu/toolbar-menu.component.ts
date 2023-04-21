import { Component , ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-toolbar-menu',
  templateUrl: './toolbar-menu.component.html',
  styleUrls: ['./toolbar-menu.component.scss']
})
export class ToolbarMenuComponent implements AfterViewInit{
  @ViewChild('menuBar', { static: true })
  menuBarRef!: ElementRef<HTMLDivElement>;
  @ViewChild('wrapper', { static: true })
  wrapperRef!: ElementRef<HTMLDivElement>;
  @ViewChild('booksButton', { static: true })
  booksButton!: ElementRef<HTMLButtonElement>;
  @ViewChild('authorButton', { static: true })
  authorButton!: ElementRef<HTMLButtonElement>;
  @ViewChild('toUp', { static: true })
  toUp!: ElementRef<HTMLDivElement>;
  @ViewChild('loginLogOutDiv', {static: true})
  loginLogOutDiv!: ElementRef<HTMLDivElement>
  @ViewChild('loginButton', {static: true})
  loginButton!: ElementRef<HTMLButtonElement>;
  constructor(
    private router: Router,
    private loginService: LoginService
  ) {}
  
  loginVisibility = true
  loginButtonText?: string

  ngOnInit(){
    if (this.loginService.isLoggedIn() === false){
      this.loginVisibility = true

    }
    else{
      this.loginVisibility = false
    }
  }
  ngAfterViewInit() {
    const menuBar = this.menuBarRef.nativeElement;
    this.onTopMenuStyle(menuBar);
    const toUp = this.toUp.nativeElement
    this.onTopToUp(toUp)
    const booksButton = this.booksButton.nativeElement;
    this.onTopBooksButtonStyle(booksButton);
    const authorButton = this.authorButton.nativeElement;
    this.onTopAuthorButtonSyle(authorButton)
    const wrapper = this.wrapperRef.nativeElement;
    const offsetTop = wrapper.offsetTop;
    const loginLogOutDiv = this.loginLogOutDiv.nativeElement;
    this.onToploginLogOutDiv(loginLogOutDiv)
    const loginButton = this.loginButton.nativeElement;
    this.onTopLoginButtonStyle(loginButton)
    window.onscroll = () => {
      if (window.pageYOffset > offsetTop) {
        this.onScrollMenuStyle(menuBar)
        this.onScrollBooksButtonStyle(booksButton)
        this.onScrollAuthorButtonSyle(authorButton)
        this.onScrollToUp(toUp)
        this.onScrollLoginButtonStyle(loginButton)
      } else {
        this.onTopMenuStyle(menuBar)
        this.onTopToUp(toUp)
        this.onTopBooksButtonStyle(booksButton)
        this.onTopAuthorButtonSyle(authorButton)
        this.onTopLoginButtonStyle(loginButton)
      }
    };
  }
  onScrollLoginButtonStyle(loginButton: HTMLButtonElement){
    loginButton.style.background = 'rgba(50, 168, 82, 0.85)'
  }

  onTopLoginButtonStyle(loginButton: HTMLButtonElement){
    if( this.loginVisibility === true ){
      this.loginButtonText = "Prisijungti"
    }
    else{
      this.loginButtonText = "Atsijungti"
    } 
    loginButton.style.margin = '15px'
    loginButton.style.backgroundColor = '#45a049'
    loginButton.style.color = 'white'
    loginButton.style.padding = '10px 20px'
    loginButton.style.border = 'none'
    loginButton.style.borderRadius = '4px'
    loginButton.style.cursor = 'pointer'

    loginButton.addEventListener('mouseover', () =>{
      loginButton.style.backgroundColor = '#4CAF50'
    })
    loginButton.addEventListener('mouseout', () => {
      loginButton.style.backgroundColor =  '#45a049'
      loginButton.style.color = 'white'
    });
    loginButton.addEventListener('click', () => {
      loginButton.style.backgroundColor = '#e7e7e7'
      loginButton.style.color = 'black'
    });

  }
  onToploginLogOutDiv(loginLogOutDiv: HTMLDivElement){
    loginLogOutDiv.style.marginLeft = 'auto'
  }

  onTopToUp(toUp: HTMLDivElement){
    toUp.style.visibility = 'hidden'
  }
  onScrollToUp(toUp: HTMLDivElement){
    toUp.style.visibility = 'visible'
    toUp.style.zIndex = '1'
    toUp.style.bottom = '0'
    toUp.style.right = '0'
    toUp.style.position = 'fixed'
    toUp.style.marginRight = '10px'
    toUp.style.padding = '10px'
    toUp.style.borderRadius = '3px'
    toUp.style.background = 'rgba(25, 118, 210, 0.7)'
    toUp.style.cursor = 'pointer'

    toUp.addEventListener('mouseover', () =>{
      toUp.style.backgroundColor = '#4CAF50'
    })
    toUp.addEventListener('mouseout', () => {
      toUp.style.backgroundColor = 'rgba(25, 118, 210, 0.7)'

    });
  }

  onScrollMenuStyle(menuBar: HTMLDivElement){
    menuBar.style.height = '60px'
    menuBar.style.backgroundColor = 'rgba(25, 118, 210, 0.7)';
  }
  onTopMenuStyle(menuBar: HTMLDivElement){
    menuBar.role = 'banner'
    menuBar.style.background = '#1976d2'
    menuBar.style.display = 'flex'
    menuBar.style.height = '80px'
    menuBar.style.width = '100%'
    menuBar.style.top = '0'
    menuBar.style.left ='0'
    menuBar.style.right = '0'
    menuBar.style.position = 'fixed'
    menuBar.style.justifyContent = 'center'
    menuBar.style.alignItems = 'center'
    menuBar.style.boxShadow = '0 8px 8px rgba(0, 0, 0, 0.3)'
    menuBar.style.zIndex = '1'
  }

  onScrollBooksButtonStyle(booksButton: HTMLButtonElement){
    booksButton.style.background = 'rgba(50, 168, 82, 0.85)'
  }
  onScrollAuthorButtonSyle(authorButton: HTMLButtonElement){
    authorButton.style.background = 'rgba(50, 168, 82, 0.85)'
  }

  onTopBooksButtonStyle(booksButton: HTMLButtonElement){
    booksButton.style.margin = '15px'
    booksButton.style.backgroundColor = '#45a049'
    booksButton.style.color = 'white'
    booksButton.style.padding = '10px 20px'
    booksButton.style.border = 'none'
    booksButton.style.borderRadius = '4px'
    booksButton.style.cursor = 'pointer'

    booksButton.addEventListener('mouseover', () =>{
      booksButton.style.backgroundColor = '#4CAF50'
    })
    booksButton.addEventListener('mouseout', () => {
      booksButton.style.backgroundColor =  '#45a049'
      booksButton.style.color = 'white'
    });
    booksButton.addEventListener('click', () => {
      booksButton.style.backgroundColor = '#e7e7e7'
      booksButton.style.color = 'black'
    });

  }
  onTopAuthorButtonSyle(authorButton: HTMLButtonElement){
    authorButton.style.margin = '15px'
    authorButton.style.backgroundColor = '#45a049'
    authorButton.style.color = 'white'
    authorButton.style.padding = '10px 20px'
    authorButton.style.border = 'none'
    authorButton.style.borderRadius = '4px'
    authorButton.style.cursor = 'pointer'
    authorButton.addEventListener('mouseover', () =>{
      authorButton.style.backgroundColor = '#4CAF50'
    })
    authorButton.addEventListener('mouseout', () => {
      authorButton.style.backgroundColor = '#45a049'
      authorButton.style.color = 'white'
    });
    authorButton.addEventListener('click', () => {
      authorButton.style.backgroundColor = '#e7e7e7'
      authorButton.style.color = 'black'
    });
  }

  onToUp(){
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
  onAutoriai(){
    this.router.navigate(['authors'])  
  }
  onKnygos(){
    this.router.navigate(['books'])  
  }

  onLogin(){
    this.router.navigate(['login'])
    
  }
  onLogOut(){
    this.router.navigate(['login'])
  }
  changeVisibilityLogOut(){
    this.loginVisibility = false
  }
}
