import React from 'react';
import PredictionList from './components/PredictionList';
import WalletConnect from './components/WalletConnect';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="p-4 bg-white shadow flex items-center justify-between"> {/* Added flex, items-center, justify-between */}
        <h1 className="text-2xl font-bold">PredictX: Bet AI Prediction on Base </h1>
        <WalletConnect />
      </header>
      <main className="container mx-auto p-4 md:pt-8"> {/* Added md:pt-8 for more space on larger screens */}
        <PredictionList />
      </main>
    </div>
  );
};

export default App;