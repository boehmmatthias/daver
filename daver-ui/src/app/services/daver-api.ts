import { HttpClient, HttpEvent } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DaverApi {
  private http = inject(HttpClient);
  
  // Base URL for API endpoints - configured via environment
  private baseUrl = environment.apiBaseUrl;

  constructor() { }

  uploadConfig(file: File): Observable<HttpEvent<any>> {
    console.log(file)
    const formData = new FormData()
    formData.append('config_file', file)

    return this.http.post(`${this.baseUrl}/upload-config`, formData, {
      reportProgress: true,
      observe: 'events'
    });
  }
} 