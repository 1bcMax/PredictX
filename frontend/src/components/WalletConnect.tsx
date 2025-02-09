import React from 'react';
import { usePrivy, useWallets } from '@privy-io/react-auth';

const WalletConnect: React.FC = () => {
  const { ready, authenticated, user, login, logout } = usePrivy();
  const { wallets } = useWallets();

  const handleConnectWallet = async () => {
    if (!authenticated) {
      await login();
    }
  };

  const handleDisconnectWallet = async () => {
    await logout();
  };

  return (
    <div>
      {ready && (
        <button
          onClick={authenticated ? handleDisconnectWallet : handleConnectWallet}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          {authenticated ? 'Disconnect Wallet' : 'Connect Wallet by Privy'}
        </button>
      )}
      {authenticated && (
        <div className="mt-4">
          <p>Connected Wallets:</p>
          <ul>
            {wallets.map((wallet) => (
              <li key={wallet.address}>{wallet.address}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default WalletConnect;