import React from 'react';
import type { Message } from '../types';
import Avatar from './Avatar';

interface MessageListProps {
  messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="space-y-4">
      {messages.map((msg) => (
        <div key={msg.id} className="flex items-start space-x-2">
          <Avatar sender={msg.sender} />
          <div className="p-3 rounded-lg bg-gray-100">
            <p className="text-sm font-semibold">{msg.sender}</p>
            <p className="text-xs text-gray-500">{new Date(msg.timestamp).toLocaleTimeString()}</p>
            <p>{msg.text}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList; 