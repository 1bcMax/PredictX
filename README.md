# PredictX
PredictX is an innovative crypto prediction battle platform where AI predictions compete with human wisdom on a level playing field.

### Core Features

AI Dynamic Predictions: Leverages advanced AI models to analyze market data and generate 24-hour price predictions
Human-AI Battle: Users can choose to support or challenge AI predictions
Smart Contract Security: All bets and reward distributions are automatically executed through smart contracts
Real-time Market Analysis: Integration with professional market data feeds for comprehensive analysis

## How It Works

### AI Prediction Generation

AI analyzes market data including price, volume, and market cap
Generates predicted price ranges with confidence levels
Provides detailed reasoning for predictions


###  User Participation

Review AI predictions and analysis rationale
Choose to support or challenge predictions
Place bets using cryptocurrency

### Settlement

Automatic price verification after 24 hours
Smart contract execution of reward distribution
Predictor reputation score updates


## Technical Stack

Frontend: React + TailwindCSS
Backend: FastAPI + Azure OpenAI
Smart Contracts: CDP AgentKit
Data Source: CoinMarketCap API

## Target Users

Crypto traders seeking data-driven insights
AI enthusiasts interested in practical applications
Investors looking for unique opportunities
Market analysts testing their strategies

## Why PredictX?

Innovative Approach: Combines AI capabilities with human insights
Transparent System: All predictions and results are recorded on-chain
Fair Play: Smart contracts ensure unbiased execution
Learning Platform: Users can improve their trading strategies by analyzing AI predictions

PredictX is more than just a prediction platform - it's an experimental arena exploring the boundaries between artificial and human intelligence in the crypto market. Whether you're a crypto expert, AI enthusiast, or investor looking for opportunities, PredictX offers a unique space to test your insights against AI predictions.


# PredictX

PredictX is an innovative crypto prediction battle platform where AI predictions compete with human wisdom.

## Features

- AI-powered price predictions
- Human-AI prediction battles
- Smart contract-based staking and rewards
- Real-time market data analysis
- On-chain result verification

## Tech Stack

- Frontend: React, TailwindCSS, ethers.js
- Backend: FastAPI, Azure OpenAI
- Smart Contracts: Solidity, CDP AgentKit
- Database: PostgreSQL
- Infrastructure: Docker, AWS

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- Docker and Docker Compose
- Metamask wallet

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/predictx.git
cd predictx
```

2. Install dependencies:
```bash
# Install root dependencies
yarn install

# Install packages dependencies
yarn workspaces run install
```

3. Set up environment variables:
```bash
# Backend
cp packages/backend/.env.example packages/backend/.env

# Frontend 
cp packages/frontend/.env.example packages/frontend/.env
```

4. Start the development environment:
```bash
# Start all services
docker-compose up -d

# Start backend
cd packages/backend
poetry run uvicorn app.main:app --reload

# Start frontend
cd packages/frontend
yarn dev
```

Visit `http://localhost:3000` to access the application.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.