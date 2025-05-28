export interface Message {
  id: string;
  text: string;
  sender: 'Pro' | 'Con' | 'Moderator';
  timestamp: string;
}

export interface DebateStatus {
  status: 'pending' | 'active' | 'finished';
  winner?: 'Pro' | 'Con';
  messages: Message[];
} 