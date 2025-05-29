import axios from 'axios';
import type { DebateStatus, Message } from '../types';

const API_URL = 'http://localhost:8000/api';

export const startDebate = async (topic: string, numRounds: number, proAgent: string, conAgent: string): Promise<{ debate_id: string, pro_agent_name?: string, con_agent_name?: string }> => {
  const response = await axios.post(`${API_URL}/start`, { 
    topic, 
    num_rounds: numRounds, 
    pro_agent_name: proAgent,
    con_agent_name: conAgent
  });
  return response.data;
};

export const getDebateContext = async (debateId: string): Promise<DebateStatus> => {
  const statusResponse = await axios.get(`${API_URL}/status/${debateId}`);
  const messagesResponse = await axios.get(`${API_URL}/context/${debateId}`);

  // Map backend messages to frontend Message type
  const feMessages: Message[] = messagesResponse.data.map((msg: any) => {
    let senderRole: 'Pro' | 'Con' | 'Moderator' | 'System' = 'System';
    if (typeof msg.role === 'string') {
      const lowerRole = msg.role.toLowerCase();
      if (lowerRole === 'pro') senderRole = 'Pro';
      else if (lowerRole === 'con') senderRole = 'Con';
      else if (lowerRole === 'mod' || lowerRole === 'moderator') senderRole = 'Moderator';
      else if (lowerRole === 'system') senderRole = 'System';
    }
    return {
      id: msg.message_id,
      text: msg.content,
      sender: senderRole,
      timestamp: msg.timestamp
    };
  });

  return {
    status: statusResponse.data.status,
    winner: statusResponse.data.winner,
    messages: feMessages
  };
};

export const getDebateStatus = async (debateId: string): Promise<{ status: 'pending' | 'active' | 'finished', winner?: 'Pro' | 'Con' }> => {
  return (await axios.get(`${API_URL}/status/${debateId}`)).data;
}; 