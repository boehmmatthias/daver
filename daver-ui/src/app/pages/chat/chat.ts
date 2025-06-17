import { Component, signal, ViewChild, ElementRef, AfterViewChecked, computed } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TextFieldModule } from '@angular/cdk/text-field';

interface ChatMessage {
  text: string;
  timestamp: Date;
  type: 'user' | 'bot';
}

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
    TextFieldModule
  ],
  templateUrl: './chat.html',
  styleUrl: './chat.scss'
})
export class Chat implements AfterViewChecked {
  @ViewChild('chatMessages') chatMessages!: ElementRef;
  
  messages = signal<ChatMessage[]>([]);
  isLoading = signal(false);
  userInput = signal('');

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

    // Simulate server response (dummy for now)
    setTimeout(() => {
      const botResponse: ChatMessage = {
        text: `I understand you're asking about: "${inputText}". This is a dummy response for now. In the real implementation, this would be the actual database query result.`,
        timestamp: new Date(),
        type: 'bot'
      };
      this.messages.update(messages => [...messages, botResponse]);
      this.isLoading.set(false);
    }, 2000);
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
