
├── README.md
├── package.json
├── packages/
│   ├── contracts/           # 智能合约
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── PredictX.sol
│   │   │   ├── Staking.sol
│   │   │   └── interfaces/
│   │   └── test/
│   ├── backend/            # FastAPI 后端
│   │   ├── requirements.txt
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── ai/
│   │   │   ├── models/
│   │   │   ├── services/
│   │   │   └── utils/
│   │   └── tests/
│   └── frontend/           # React 前端
│       ├── package.json
│       ├── public/
│       └── src/
│           ├── components/
│           ├── hooks/
│           ├── services/
│           ├── store/
│           ├── types/
│           └── utils/
└── docker/                 # Docker配置
    ├── docker-compose.yml
    └── Dockerfile.backend