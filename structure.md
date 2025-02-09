predictX/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI app + 主要逻辑
│   │   ├── models.py              # 所有数据模型
│   │   ├── ai_engine.py           # AI预测逻辑
│   │   └── utils.py               # 工具函数
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx               # 主应用
│   │   ├── components/
│   │   │   ├── PredictionCard.tsx    # 预测卡片
│   │   │   ├── PredictionList.tsx    # 预测列表
│   │   │   └── WalletConnect.tsx     # 钱包连接
│   │   ├── services/
│   │   │   └── api.ts            # API调用
│   │   └── types.ts              # 类型定义
│   ├── package.json
│   └── README.md
│
└── README.md