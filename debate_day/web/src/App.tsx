import React from 'react';
import './index.css';
import { useDebate } from './hooks/useDebate';
import MessageList from './components/MessageList';
import Controls from './components/Controls';

function App() {
  const { messages, status, winner, loading, error, startDebate, restartDebate } = useDebate();

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-3xl font-bold text-center mb-8">Debate Day 2.0</h1>

      <Controls 
        onStartDebate={startDebate} 
        onRestartDebate={restartDebate} 
        status={status} 
        loading={loading} 
      />

      {error && <p className="text-red-500 text-center my-4">Error: {error}</p>}

      {status === 'active' && messages.length === 0 && !loading && (
        <p className="text-center my-4">Debate is starting... waiting for messages.</p>
      )}

      {messages.length > 0 && (
        <div className="my-8">
          <MessageList messages={messages} />
        </div>
      )}

      {status === 'finished' && winner && (
        <div className="my-8 p-4 bg-green-100 rounded-lg text-center">
          <h2 className="text-2xl font-semibold">Debate Finished!</h2>
          <p className="text-xl">Winner: <span className="font-bold">{winner}</span></p>
        </div>
      )}
       {status === 'finished' && !winner && (
        <div className="my-8 p-4 bg-yellow-100 rounded-lg text-center">
          <h2 className="text-2xl font-semibold">Debate Finished!</h2>
          <p className="text-xl">The debate ended without a clear winner.</p>
        </div>
      )}
    </div>
  );
}

export default App;
