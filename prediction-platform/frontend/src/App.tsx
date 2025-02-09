import React from 'react';
import PredictionList from './components/PredictionList';
import WalletConnect from './components/WalletConnect';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="p-4 bg-white shadow">
        <h1 className="text-2xl font-bold">PredictX: Bet AI Prediction on Base </h1>
        <WalletConnect />
      </header>
      <main className="container mx-auto p-4">
        <PredictionList />
      </main>
    </div>
  );
};

export default App;
