# Healthcare Assistant — Microsoft Foundry Prompt Agent

A Microsoft Foundry prompt agent that acts as a healthcare assistant, backed by an Azure OpenAI model deployment. Built with the **Microsoft Agent Framework** SDK.

## Capabilities

- General health and wellness information
- Common symptom explanation and guidance
- Preventive-care tips (nutrition, exercise, sleep, stress)
- Publicly available medication information
- Guidance on when to seek professional medical attention

> **Disclaimer:** This agent is an AI assistant and does **not** replace professional medical advice, diagnosis, or treatment.

## Prerequisites

- Python 3.10+
- An [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/) project with an Azure OpenAI model deployment (e.g. `gpt-4o`)
- Azure CLI authenticated (`az login`)

## Quick Start

### 1. Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.template` to `.env` and fill in your values:

```
FOUNDRY_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o
# Azure OpenAI Service connection name configured in your Foundry project
AZURE_OPENAI_CONNECTION_NAME=
```

### 4. Run the agent

```bash
python app.py
```

The agent starts an HTTP server on port **8088** exposing the OpenAI Responses API.

### 5. Test

```bash
curl -X POST http://localhost:8088/responses \
  -H "Content-Type: application/json" \
  -d '{"input": "What are some tips for better sleep?"}'
```

## Debugging

This project includes VS Code launch configurations for interactive debugging with the **AI Toolkit Agent Inspector**:

1. Install the [AI Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio) VS Code extension.
2. Open this folder in VS Code.
3. Press **F5** to start the *Debug Healthcare Agent (HTTP Server)* configuration.

## Deploy to Foundry

Build and push the container, then create the agent using the Foundry CLI or MCP tools. See the [Hosted Agents docs](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents) for details.

```bash
docker build --platform linux/amd64 -t healthcare-assistant .
```

## Project Structure

```
healthcare-agent/
├── .env.template            # Environment variable template
├── .foundry/
│   └── agent-metadata.yaml  # Foundry workspace metadata
├── .gitignore
├── .vscode/
│   ├── launch.json          # VS Code debug configuration
│   └── tasks.json           # VS Code tasks (agentdev + inspector)
├── agent.yaml               # Foundry agent definition
├── app.py                   # Agent entrypoint
├── Dockerfile               # Container image for deployment
├── README.md
└── requirements.txt         # Python dependencies
```

## SDK Versions

| Package | Version |
|---------|---------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
