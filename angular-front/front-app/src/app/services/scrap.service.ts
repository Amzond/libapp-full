import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ScrapService {

  constructor(private http: HttpClient) {}

  private scrap_url = 'http://127.0.0.1:8000/api/scrape/'
  scrapeDataVaga(data?: any) {

    return this.http.post(this.scrap_url, data)
  }
}
