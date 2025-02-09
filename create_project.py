import os
import json

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_project_structure():
    # Root directory
    root_dir = "predictx"
    create_directory(root_dir)

    # Root files
    write_file(f"{root_dir}/README.md", """# PredictX

PredictX is an innovative crypto prediction battle platform where AI predictions compete with human wisdom.

## Features
- AI-powered price predictions
- Human-AI prediction battles
- Smart contract-based staking and rewards
- Real-time market data analysis
""")

    write_file(f"{root_dir}/package.json", """{
  "name": "predictx",
  "version": "1.0.0",
  "private": true,
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "dev": "yarn workspaces run dev",
    "build": "yarn workspaces run build",
    "test": "yarn workspaces run test"
  }
}""")

    # Contracts
    contracts_dir = f"{root_dir}/packages/contracts"
    create_directory(contracts_dir)
    create_directory(f"{contracts_dir}/src")
    create_directory(f"{contracts_dir}/src/interfaces")
    create_directory(f"{contracts_dir}/test")

    write_file(f"{contracts_dir}/package.json", """{
  "name": "@predictx/contracts",
  "version": "1.0.0",
  "scripts": {
    "compile": "hardhat compile",
    "test": "hardhat test",
    "deploy": "hardhat deploy"
  },
  "dependencies": {
    "@openzeppelin/contracts": "^4.9.0",
    "hardhat": "^2.17.0"
  }
}""")

    # Already provided Solidity contract
    write_file(f"{contracts_dir}/src/PredictX.sol", """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract PredictX is ReentrancyGuard, Ownable {
    // Contract implementation
}""")

    # Backend
    backend_dir = f"{root_dir}/packages/backend"
    create_directory(backend_dir)
    create_directory(f"{backend_dir}/app")
    create_directory(f"{backend_dir}/app/ai")
    create_directory(f"{backend_dir}/app/models")
    create_directory(f"{backend_dir}/app/services")
    create_directory(f"{backend_dir}/app/utils")
    create_directory(f"{backend_dir}/tests")

    write_file(f"{backend_dir}/requirements.txt", """fastapi==0.100.0
uvicorn==0.22.0
python-dotenv==1.0.0
openai==1.3.0
sqlalchemy==2.0.20
pydantic==2.1.1
pytest==7.4.0
web3==6.8.0""")

    write_file(f"{backend_dir}/app/main.py", """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PredictX API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to PredictX API"}""")

    # Frontend
    frontend_dir = f"{root_dir}/packages/frontend"
    create_directory(frontend_dir)
    create_directory(f"{frontend_dir}/public")
    create_directory(f"{frontend_dir}/src")
    create_directory(f"{frontend_dir}/src/components")
    create_directory(f"{frontend_dir}/src/hooks")
    create_directory(f"{frontend_dir}/src/services")
    create_directory(f"{frontend_dir}/src/store")
    create_directory(f"{frontend_dir}/src/types")
    create_directory(f"{frontend_dir}/src/utils")

    write_file(f"{frontend_dir}/package.json", """{
  "name": "@predictx/frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "ethers": "^6.6.4",
    "@web3-react/core": "^8.2.0",
    "tailwindcss": "^3.3.3"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "typescript": "^5.0.2",
    "vite": "^4.4.5"
  }
}""")

    # Docker
    docker_dir = f"{root_dir}/docker"
    create_directory(docker_dir)

    write_file(f"{docker_dir}/docker-compose.yml", """version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/predictx
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=predictx
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:""")

    write_file(f"{docker_dir}/Dockerfile.backend", """FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]""")

if __name__ == "__main__":
    create_project_structure()
    print("Project structure created successfully!")