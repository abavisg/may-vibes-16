import axios from 'axios';
import type { DebateStatus, Message } from '../types';

const API_URL = 'http://localhost:8000/api';

export const startDebate = async (topic: string, numRounds: number, proAgent: string, conAgent: string): Promise<{ debate_id: string, pro_agent_name?: string, con_agent_name?: string }> => {
  // console.log('Starting debate:', { topic, numRounds, proAgent, conAgent });
  // return new Promise((resolve) => setTimeout(() => resolve({ debate_id: 'mock_debate_id' }), 1000));
  const response = await axios.post(`${API_URL}/start`, { 
    topic, 
    num_rounds: numRounds, 
    pro_agent_name: proAgent, // Ensure backend expects pro_agent_name
    con_agent_name: conAgent   // Ensure backend expects con_agent_name
  });
  return response.data; // Should contain debate_id and potentially agent names
};

export const getDebateContext = async (debateId: string): Promise<DebateStatus> => {
  // console.log('Getting debate context for:', debateId);
  // const mockMessages: Message[] = [
  //   { id: '1', text: 'Hello from Pro!', sender: 'Pro' as const, timestamp: new Date().toISOString() },
  //   { id: '2', text: 'Hello from Con!', sender: 'Con' as const, timestamp: new Date().toISOString() },
  // ];
  // return new Promise((resolve) => setTimeout(() => resolve({ status: 'active', messages: mockMessages }), 1000));
  const response = await axios.get(`${API_URL}/context/${debateId}`);
  // The backend /api/context/{debate_id} returns List[Dict[str, Any]] which are MCPMessageRecord.dict()
  // We need to map this to the frontend Message[] type and assume a DebateStatus structure.
  // This might require adjustment based on actual API response from /context/ and /status/
  // For now, let's assume /context/ gives us messages and we get status separately if needed, 
  // or that /context/ somehow implies active status with messages.
  // A better approach would be for /context/ or a combined status endpoint to return DebateStatus directly.
  
  // Let's assume the actual /api/context endpoint returns the full DebateStatus structure or enough to build it.
  // If it only returns messages, we might need to call /api/status separately and combine.
  // For now, attempting to cast, but this will LIKELY NEED REFINEMENT based on actual API structure.
  
  // Fetching full status to construct the DebateStatus object properly
  const statusResponse = await axios.get(`${API_URL}/status/${debateId}`);
  const messagesResponse = await axios.get(`${API_URL}/context/${debateId}`);

  // Map backend messages (MCPMessageRecord.dict()) to frontend Message type
  const feMessages: Message[] = messagesResponse.data.map((msg: any) => {
    let senderRole: 'Pro' | 'Con' | 'Moderator' | 'System' = 'System'; // Default to System for safety
    if (typeof msg.role === 'string') {
      const lowerRole = msg.role.toLowerCase();
      if (lowerRole === 'pro') senderRole = 'Pro';
      else if (lowerRole === 'con') senderRole = 'Con';
      else if (lowerRole === 'mod' || lowerRole === 'moderator') senderRole = 'Moderator';
      else if (lowerRole === 'system') senderRole = 'System';
      // If msg.role is something else, it remains 'System' as per initialization
    }
    
    // For Avatar display, map System to Moderator or handle differently
    // For now, let's ensure AvatarProps.sender type matches what Avatar expects
    let avatarSender: 'Pro' | 'Con' | 'Moderator' = 'Moderator'; // Default for Avatar
    if (senderRole === 'Pro') avatarSender = 'Pro';
    else if (senderRole === 'Con') avatarSender = 'Con';
    // System messages could use a generic avatar, let's use Moderator's for now if not System
    // Or we update Avatar component to accept 'System' if we want a distinct one

    return {
      id: msg.message_id,
      text: msg.content,
      sender: senderRole, // This now correctly matches the updated Message.sender type
      timestamp: msg.timestamp
    };
  }); 

  return {
    status: statusResponse.data.status, // e.g., 'active', 'finished'
    winner: statusResponse.data.winner,
    messages: feMessages
  };
};

export const getDebateStatus = async (debateId: string): Promise<{ status: 'pending' | 'active' | 'finished', winner?: 'Pro' | 'Con' }> => {
  // console.log('Getting debate status for:', debateId);
  // return new Promise((resolve) => setTimeout(() => resolve({ status: 'finished', winner: 'Pro' as const }), 1000));
  const response = await axios.get(`${API_URL}/status/${debateId}`);
  return response.data; // This should match the expected return type
}; 