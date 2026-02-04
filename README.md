# selfhosted-n8n-local-llm

Self-hosted **n8n + Ollama (Llama3.2)** stack for **8GB M1/M2 Macs**.

**One-command AI automation!** 🤖

## 🚀 Quick Start

```bash
# 1. Clone & setup
git clone https://github.com/sanjay-rb/selfhosted-n8n-local-llm.git
cd selfhosted-n8n-local-llm

# 2. Make init script executable (required for PostgreSQL setup)
chmod +x init-data.sh

# 3. Start stack
docker compose up -d

# 4. Install Ollama model (one-time, 2-5min)
docker exec ollama ollama pull llama3.2:3b

# 5. Access:
# n8n: http://localhost:5678
# Ollama API: http://localhost:11434
```

## 📁 Folder Structure

```
selfhosted-n8n-local-llm/
├── docker-compose.yml      # Complete stack
├── README.md              # This file
└── n8n_data/              # Persistent (auto-created)
```

## 🎯 **Usage Examples**

### **1. n8n Workflow: Ollama Chat**
```
Manual Trigger → Ollama Chat
Prompt: "Hello, how are you?"
```

### **2. n8n Ollama Settings**
```
Ollama Chat Model Node:
✅ Base URL: http://ollama:11434
✅ Model: llama3.2:3b (EXACT TAG)
```

## 📊 **Services**

| Service | Port | Purpose | First Run |
|---------|------|---------|-----------|
| **n8n** | 5678 | Workflow automation | Instant |
| **Ollama** | 11434 | Llama3.2:3b (2GB) | 2-5min download |

## 💾 **Persistent Storage**
```
n8n_data/          # Workflows
ollama_data/       # Llama3.2 model (2GB+)
```

## ⚙️ **Hardware Requirements**
- ✅ **8GB RAM M1/M2 Mac** (tested)
- ✅ **16GB+** = faster responses

## ⏱️ **Performance (8GB M1 Mac)**
```
Ollama response: 10-60 seconds
n8n workflows: Instant
RAM usage: ~3-4GB peak
```

## 🔧 **Troubleshooting**

### **PostgreSQL: "password authentication failed"?**
```bash
# Ensure init-data.sh is executable:
chmod +x init-data.sh

# Then restart:
docker compose down -v
docker compose up -d
```

### **Ollama "model not found"?**
```bash
docker exec ollama ollama pull llama3.2:3b
# In n8n: use EXACT "llama3.2:3b" (no :latest)
```

### **n8n can't reach Ollama?**
```
Use http://ollama:11434 (not localhost)
Services communicate via shared 'backend' Docker network
```

### **Clean restart:**
```bash
docker compose down -v
chmod +x init-data.sh
docker compose up -d
docker exec ollama ollama pull llama3.2:3b
```

## 🎨 **Example n8n Workflow**

```
1. Manual Trigger
2. Ollama Chat: "Suggest a productivity tip"
3. Email/Slack: "{{ $('Ollama').item.json.response }}"
```

## 📱 **Access URLs**
```
n8n UI: http://localhost:5678
Ollama API: http://localhost:11434/api/tags
```

## 🚀 **Production Ready**
- ✅ Persistent storage
- ✅ Auto-restart
- ✅ London timezone
- ✅ n8n Runners enabled
- ✅ 8GB RAM optimized