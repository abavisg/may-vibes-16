import { useState, useEffect, useCallback } from 'react';
import type { Message, DebateStatus } from '../types';
import { startDebate as apiStartDebate, getDebateContext as apiGetDebateContext, getDebateStatus as apiGetDebateStatus } from '../api/mcp';

export const useDebate = () => {
  const [debateId, setDebateId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [status, setStatus] = useState<'pending' | 'active' | 'finished'>('pending');
  const [winner, setWinner] = useState<'Pro' | 'Con' | undefined>(undefined);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startDebate = useCallback(async (topic: string, numRounds: number, proAgent: string, conAgent: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiStartDebate(topic, numRounds, proAgent, conAgent);
      setDebateId(data.debate_id);
      setMessages([]);
      setStatus('active');
      setWinner(undefined);
    } catch (err) {
      setError('Failed to start debate');
      console.error(err);
    }
    setLoading(false);
  }, []);

  const restartDebate = useCallback(() => {
    setDebateId(null);
    setMessages([]);
    setStatus('pending');
    setWinner(undefined);
    setError(null);
  }, []);

  useEffect(() => {
    if (!debateId || status === 'finished') return;

    const pollInterval = setInterval(async () => {
      try {
        const contextData = await apiGetDebateContext(debateId);
        setMessages(contextData.messages);
        setStatus(contextData.status);

        if (contextData.status === 'finished') {
          const statusData = await apiGetDebateStatus(debateId);
          setWinner(statusData.winner);
          clearInterval(pollInterval); 
        }
      } catch (err) {
        setError('Failed to fetch debate updates');
        console.error(err);
        clearInterval(pollInterval); 
      }
    }, 3000);

    return () => clearInterval(pollInterval);
  }, [debateId, status]);

  return { debateId, messages, status, winner, loading, error, startDebate, restartDebate };
}; 