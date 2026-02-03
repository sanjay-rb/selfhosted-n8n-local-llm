# AI Coding Agent Instructions for selfhosted-n8n-local-llm

## Project Overview
Self-hosted AI automation stack combining n8n workflows and local Ollama LLM. Optimized for 8GB M1/M2 Macs using Docker Compose microservices.

## Architecture
- **n8n** (port 5678): Workflow orchestration and UI
- **Ollama** (port 11434): Local Llama3.2:3b inference

Data flows: n8n workflows call Ollama API for text generation and analysis.

## Critical Workflows
### Setup Sequence
```bash
git clone <repo>
cd selfhosted-n8n-local-llm
docker compose up -d
docker exec ollama ollama pull llama3.2:3b
```

### Model Management
- Use exact tag `llama3.2:3b` (not `:latest`)
- First run downloads ~2GB model
- Monitor with `docker logs ollama` for completion

### Service Communication
- In n8n workflows: Use `http://ollama:11434` (service name, not localhost)
- Example: Ollama Chat node for text generation

## Project Conventions
### Docker Compose
- Persistent volumes: `n8n_data`, `ollama_data`
- Environment: `GENERIC_TIMEZONE: "Europe/London"`, `N8N_RUNNERS_ENABLED: "true"`
- Restart policy: `unless-stopped`

### Workflows
- Stored as JSON files (e.g., `Today's Penny Stock.json`)
- Use n8n nodes: ManualTrigger, SerpAPI, LangChain Agent, LangChain Chain LLM, Code (JavaScript), Ollama Chat Model, Telegram
- Integrate external APIs (SerpAPI for search, Telegram for notifications) with local Ollama
- Data processing: Use JavaScript Code nodes for JSON manipulation and text extraction
- Prompt engineering: Define system messages and prompts for financial analysis and recommendations
- Credentials: Set up API keys for SerpAPI, Telegram, Ollama

## Key Files
- `docker-compose.yml`: Service definitions and volumes
- `README.md`: Complete setup, troubleshooting, and usage examples
- Workflow JSONs: n8n automation examples (e.g., penny stock analysis with search, LLM processing, and messaging)

## Troubleshooting Patterns
- Service unreachable: Use Docker service names in URLs
- Model not found: `docker exec ollama ollama pull llama3.2:3b`
- Clean restart: `docker compose down -v && docker compose up -d`</content>
<parameter name="filePath">/Users/sanjayrb/projects/selfhosted-n8n-local-llm/.github/copilot-instructions.md