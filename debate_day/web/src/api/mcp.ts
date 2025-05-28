import axios from 'axios';
import type { DebateStatus } from '../types';

const API_URL = 'http://localhost:8000/api';

export const startDebate = async (topic: string, numRounds: number, proAgent: string, conAgent: string): Promise<{ debate_id: string }> => {
  // Placeholder: Replace with actual API call
  console.log('Starting debate:', { topic, numRounds, proAgent, conAgent });
  return new Promise((resolve) => setTimeout(() => resolve({ debate_id: 'mock_debate_id' }), 1000));
  // const response = await axios.post(`${API_URL}/start`, { topic, num_rounds: numRounds, pro_agent: proAgent, con_agent: conAgent });
  // return response.data;
};

export const getDebateContext = async (debateId: string): Promise<DebateStatus> => {
  // Placeholder: Replace with actual API call
  console.log('Getting debate context for:', debateId);
  const mockMessages = [
    { id: '1', text: 'Hello from Pro!', sender: 'Pro' as const, timestamp: new Date().toISOString() },
    { id: '2', text: 'Hello from Con!', sender: 'Con' as const, timestamp: new Date().toISOString() },
  ];
  return new Promise((resolve) => setTimeout(() => resolve({ status: 'active', messages: mockMessages }), 1000));
  // const response = await axios.get(`${API_URL}/context/${debateId}`);
  // return response.data;
};

export const getDebateStatus = async (debateId: string): Promise<{ status: 'pending' | 'active' | 'finished', winner?: 'Pro' | 'Con' }> => {
  // Placeholder: Replace with actual API call
  console.log('Getting debate status for:', debateId);
  return new Promise((resolve) => setTimeout(() => resolve({ status: 'finished', winner: 'Pro' as const }), 1000));
  // const response = await axios.get(`${API_URL}/status/${debateId}`);
  // return response.data;
}; 