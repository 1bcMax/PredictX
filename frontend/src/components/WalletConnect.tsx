import React, { useState } from 'react';

const WalletConnect: React.FC = () => {
  const [connected, setConnected] = useState(false);

  const connectWallet = async () => {
    setConnected(true);
  };

  return (
    <button 
      onClick={connectWallet}
      className="bg-blue-500 text-white px-4 py-2 rounded"
    >
      {connected ? 'Connected' : 'Connect Wallet'}
    </button>
  );
};

export default WalletConnect;
