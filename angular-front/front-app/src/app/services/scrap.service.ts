import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ScrapService {

  constructor(private http: HttpClient) {}

  private scrap_url = 'http://127.0.0.1:8000/api/scrape/'
  scrapeData(data?: any): Observable<any> {
    return this.http.post(this.scrap_url, data)
  }
  private scrap_single_vaga = 'http://127.0.0.1:8000/api/scrap-single-book/'
  scrapeSingleBook(data?: any): Observable<any>{
    return this.http.post(this.scrap_single_vaga, data)
  }

}
