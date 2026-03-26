# AI_Gateway 🤖 - Smart LLM Router

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A research-driven AI gateway that intelligently routes prompts to the most appropriate LLM based on complexity—balancing cost, speed, and quality.

---

## 🎯 Research Question

**Does smarter routing actually work, or does it secretly hurt quality?**

This project evaluates whether a routing model can reduce costs without sacrificing response quality.

---

## 📊 Key Results

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Routing Accuracy | >75% | **100%** | ✅ |
| Cost Savings | >25% | **57%** | ✅ |
| Cache Hit Rate | >15% | **18.5%** | ✅ |
| Routing Latency | - | **<10ms** | ✅ |

---

## 🏗️ Architecture

```
USER REQUEST (POST /chat)
        │
        ▼
CACHE LAYER (Semantic Similarity: 0.85)
        │
   HIT ─┴─ MISS
    │        │
    ▼        ▼
Cached   ROUTING MODEL
Response  (Complexity Score)
              │
              ▼
       MODEL SELECTION
        │           │
        ▼           ▼
 FAST MODEL     CAPABLE MODEL
 (Groq LLaMA)   (Gemini Pro)
  <1s, cheaper   ~3s, stronger
        │           │
        └──────┬────┘
               ▼
     RESPONSE + METADATA
```

---

## 📁 Project Structure

```
ai-gateway/
│
├── src/
│   ├── __init__.py
│   ├── gateway.py
│   ├── routing_model.py
│   ├── cache.py
│   ├── models.py
│   └── logger.py
│
├── logs/
│   └── gateway_logs.json
│
├── poc.py
├── full_demo.py
├── test_suite.json
├── log_viewer.html
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- (Optional) API Keys:
  - Groq API
  - Google Gemini API

---

### Installation

#### 1. Clone the repo
```bash
git clone https://github.com/yourusername/ai-gateway.git
cd ai-gateway
```

#### 2. Install dependencies
```bash
pip install -r requirements.txt
```

#### 3. Setup environment

Add keys:
```
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
```

#### 4. Run server
```bash
python -m uvicorn src.gateway:app --reload
```

#### 5. Test
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"prompt":"What is 2+2?"}'
```

---

## 📡 API Endpoints

### POST `/chat`

**Request**
```json
{
  "prompt": "What is the capital of France?"
}
```

**Response**
```json
{
  "response": "Paris",
  "model_used": "fast",
  "routing_reason": "Simple query detected",
  "confidence_score": 0.90,
  "latency_ms": 18.5,
  "cache_hit": false,
  "request_id": "abc-123"
}
```

---

### GET `/logs`

Returns all request logs.

---

### GET `/health`

```json
{
  "status": "healthy",
  "routing_model": {
    "type": "rule-based",
    "threshold": 0.5
  },
  "cache": {
    "size": 12,
    "hit_rate": 0.156
  }
}
```

---

## 🧪 Testing

### Run PoC
```bash
python poc.py
```

### Python Test
```bash
python full_demo.py
```

---

## 🎬 Demo Flow (1 Minute)

- Run `poc.py` → shows accuracy  
- Start server  
- Test simple → FAST  
- Test complex → CAPABLE  
- Show cache hit  
- Open logs  

---

## 🔬 Routing Model

### Complexity Types

| Type | Examples |
|------|---------|
| Simple | "What is 2+2?" |
| Complex | "Explain quantum computing" |

---

### Features

| Signal | Weight |
|--------|--------|
| Keywords | 35% |
| Structure | 25% |
| Syntax | 20% |
| Length | 20% |

---

### Decision Logic

```
IF complex keywords → CAPABLE
ELIF simple keywords & short → FAST
ELIF long prompt → CAPABLE
ELIF short prompt → FAST
ELSE → FAST
```

---

## 📀 Cache Layer

- Method: Semantic similarity  
- Threshold: 0.85  
- Size: 1000 (LRU)  

### Performance

| Scenario | Latency |
|----------|--------|
| Hit | ~12ms |
| Miss | ~850ms |

---

## 💰 Cost Analysis

### Pricing (per 1M tokens)

| Model | Cost |
|------|------|
| FAST | $0.10 |
| CAPABLE | $0.35 |

### Savings

| Strategy | Cost |
|----------|------|
| Always CAPABLE | $0.042 |
| Smart Routing | $0.018 |

**Savings: ~57%**

---

## 🔧 Troubleshooting

### Port issue
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Check API keys
```bash
python -c "import os; print(os.getenv('GROQ_API_KEY'))"
```

---

## 📚 Methodology

- Defined complexity via reasoning needs  
- Used rule-based model for transparency  
- Evaluated on 20 labeled prompts  
- Optimized for latency and explainability  

---

## 🔮 Future Improvements

- Adaptive routing thresholds  
- Embedding-based cache  
- Multi-model support  
- Analytics dashboard  
- Authentication & rate limiting  

---

## 📄 License

MIT License
