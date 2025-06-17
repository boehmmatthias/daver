import { Component, signal, ViewChild, ElementRef, AfterViewChecked, computed, inject } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TextFieldModule } from '@angular/cdk/text-field';
import { DaverApi } from '../../services/daver-api';
import { ChatMessage } from '../../models/chat.model';
import { DataTable } from '../../components/data-table/data-table';

@Component({
  selector: 'daver-chat',
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    TextFieldModule,
    DataTable
  ],
  templateUrl: './chat.html',
  styleUrl: './chat.scss'
})
export class Chat implements AfterViewChecked {
  @ViewChild('chatMessages') chatMessages!: ElementRef;

  messages = signal<ChatMessage[]>([]);
  isLoading = signal(false);
  userInput = signal('');
  errorMessage = signal<string | null>(null);

  private daverApi = inject(DaverApi);

  // Computed property to get all messages in chronological order
  allMessages = computed(() => {
    return this.messages().sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());
  });

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      if (event.shiftKey) {
        // Shift+Enter creates a new line (default behavior)
        return;
      } else {
        // Enter sends the message
        event.preventDefault();
        this.sendMessage();
      }
    }
  }

  sendMessage(): void {
    if (!this.userInput().trim() || this.isLoading()) {
      return;
    }

    // Clear any previous errors
    this.errorMessage.set(null);

    // Add user message
    const userMessage: ChatMessage = {
      text: this.userInput().trim(),
      timestamp: new Date(),
      type: 'user'
    };
    this.messages.update(messages => [...messages, userMessage]);

    // Clear input
    const inputText = this.userInput();
    this.userInput.set('');

    // Show loading state
    this.isLoading.set(true);

    // Send message to server
    this.daverApi.sendChatMessage(inputText).subscribe({
      next: (response) => {
        // Extract the result array from fetched_data
        const resultData = response.fetched_data?.result || [];
        const hasData = Array.isArray(resultData) && resultData.length > 0;
        const hasAdditionalInfo = response.additional_information && response.additional_information.trim();
        
        // Determine what text to show
        let botText = '';
        if (hasData) {
          // If we have data, show success message or additional info
          botText = hasAdditionalInfo ? response.additional_information : 'Here are the results:';
        } else {
          // If no data, show appropriate message
          botText = hasAdditionalInfo ? response.additional_information : 'No data found for your query.';
        }
        
        const botResponse: ChatMessage = {
          text: botText,
          timestamp: new Date(),
          type: 'bot',
          fetchedData: hasData ? resultData : undefined
        };
        this.messages.update(messages => [...messages, botResponse]);
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Chat message failed:', error);
        this.isLoading.set(false);
        
        // Add error message from bot
        const errorResponse: ChatMessage = {
          text: this.getErrorMessage(error),
          timestamp: new Date(),
          type: 'bot'
        };
        this.messages.update(messages => [...messages, errorResponse]);
      }
    });
  }

  private getErrorMessage(error: any): string {
    if (error.status === 0) {
      return 'Network error. Please check your connection and try again.';
    } else if (error.status === 400) {
      return 'Invalid message format. Please try rephrasing your question.';
    } else if (error.status >= 500) {
      return 'Server error. Please try again later.';
    } else {
      return 'Sorry, I encountered an error. Please try again.';
    }
  }

  private scrollToBottom(): void {
    try {
      const element = this.chatMessages.nativeElement;
      element.scrollTop = element.scrollHeight;
    } catch (err) {
      // Handle error if element is not available
    }
  }
}
