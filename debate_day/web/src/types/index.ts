export interface Message {
  id: string;
  text: string;
  sender: 'Pro' | 'Con' | 'Moderator' | 'System';
  timestamp: string;
}

export interface DebateStatus {
  status: 'pending' | 'active' | 'finished';
  winner?: 'Pro' | 'Con';
  messages: Message[];
} 