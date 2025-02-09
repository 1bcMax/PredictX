import React from 'react';
import { createRoot } from 'react-dom/client';
import { PrivyProvider } from '@privy-io/react-auth'; // Import PrivyProvider
import './index.css';
import App from './App';

const container = document.getElementById('root');
if (!container) throw new Error('Failed to find the root element');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <PrivyProvider
      appId="cm6cbxqxp00gdc4ojtikfxkkz" // Replace with your Privy App ID
      config={{
        // Optional: Customize Privy's behavior
        loginMethods: ['email', 'wallet'], // Enable email and wallet login
        embeddedWallets: {
          createOnLogin: 'all-users', // Automatically create embedded wallets for all users
        },
      }}
    >
      <App />
    </PrivyProvider>
  </React.StrictMode>
);