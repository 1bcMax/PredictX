import React from 'react';
import { CdpAgentkit } from '@coinbase/agentkit';
import PredictionList from './components/PredictionList';
import WalletConnect from './components/WalletConnect';

const agentkit = new CdpAgentkit({
  apiKeyName: process.env.REACT_APP_CDP_API_KEY_NAME,
  privateKey: process.env.REACT_APP_CDP_API_KEY_PRIVATE_KEY
});

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="p-4 bg-white shadow">
        <h1 className="text-2xl font-bold">PredictX</h1>
        <WalletConnect agentkit={agentkit} />
      </header>
      <main className="container mx-auto p-4">
        <PredictionList agentkit={agentkit} />
      </main>
    </div>
  );
};

export default App;
