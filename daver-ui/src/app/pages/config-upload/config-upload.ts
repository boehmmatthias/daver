import { Component, signal } from '@angular/core';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'daver-config-upload',
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './config-upload.html',
  styleUrl: './config-upload.scss'
})
export class ConfigUpload {
  selectedFile = signal<File | null>(null);
  isDragOver = signal(false);
  isUploading = signal(false);
  isAnalyzing = signal(false);

  constructor(private router: Router) {}

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver.set(true);
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver.set(false);
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver.set(false);
    
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  onFileSelected(event: Event): void {
    const target = event.target as HTMLInputElement;
    const files = target.files;
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  private handleFile(file: File): void {
    // Check if file type is supported
    const supportedTypes = ['.yaml'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (supportedTypes.includes(fileExtension)) {
      this.selectedFile.set(file);
    } else {
      // You might want to show an error message here
      console.error('Unsupported file type');
    }
  }

  removeFile(): void {
    this.selectedFile.set(null);
  }

  uploadConfig(): void {
    const file = this.selectedFile();
    if (!file) return;
    
    this.isUploading.set(true);
    
    // Simulate upload process with modern timing
    setTimeout(() => {
      this.isUploading.set(false);
      this.isAnalyzing.set(true);
      
      // Simulate database analysis
      setTimeout(() => {
        this.isAnalyzing.set(false);
        // Navigate to chat component
        this.router.navigate(['/chat']);
      }, 8000); // 8 seconds for analysis simulation
    }, 3000); // 3 seconds for upload simulation
  }
}
