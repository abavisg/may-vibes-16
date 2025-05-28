import React, { useState } from 'react';

interface ControlsProps {
  onStartDebate: (topic: string, numRounds: number, proAgent: string, conAgent: string) => void;
  onRestartDebate: () => void;
  status: 'pending' | 'active' | 'finished';
  loading: boolean;
}

const Controls: React.FC<ControlsProps> = ({ onStartDebate, onRestartDebate, status, loading }) => {
  const [topic, setTopic] = useState('AI in Education');
  const [numRounds, setNumRounds] = useState(3);
  const [proAgent, setProAgent] = useState('ProAgent1');
  const [conAgent, setConAgent] = useState('ConAgent1');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onStartDebate(topic, numRounds, proAgent, conAgent);
  };

  return (
    <div className="p-4 bg-gray-50 rounded-lg shadow">
      {status === 'pending' && (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="topic" className="block text-sm font-medium text-gray-700">Debate Topic</label>
            <input type="text" id="topic" value={topic} onChange={(e) => setTopic(e.target.value)} className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
          </div>
          <div>
            <label htmlFor="numRounds" className="block text-sm font-medium text-gray-700">Number of Rounds</label>
            <input type="number" id="numRounds" value={numRounds} onChange={(e) => setNumRounds(parseInt(e.target.value))} className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
          </div>
          <div>
            <label htmlFor="proAgent" className="block text-sm font-medium text-gray-700">Pro Agent Name</label>
            <input type="text" id="proAgent" value={proAgent} onChange={(e) => setProAgent(e.target.value)} className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
          </div>
          <div>
            <label htmlFor="conAgent" className="block text-sm font-medium text-gray-700">Con Agent Name</label>
            <input type="text" id="conAgent" value={conAgent} onChange={(e) => setConAgent(e.target.value)} className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
          </div>
          <button type="submit" disabled={loading} className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50">
            {loading ? 'Starting...' : 'Start Debate'}
          </button>
        </form>
      )}
      {(status === 'active' || status === 'finished') && (
        <button onClick={onRestartDebate} className="w-full bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
          Restart Debate
        </button>
      )}
    </div>
  );
};

export default Controls; 