# Pokedex CLI — Modular Edition 🚀

An agentic Pokedex terminal application built with **LangGraph**, utilizing the **Model Context Protocol (MCP)** to orchestrate tool-calling between a cloud-hosted LLM and a local **MongoDB** database.

## 🏗️ System Architecture

The project is split into two primary components running in a containerized environment:
1.  **Client (`langgraph-client`)**: Houses the LangGraph state machine, the terminal UI, and the MCP client logic. It connects to cloud LLMs via the OpenAI-compatible adapter.
2.  **Server (MCP)**: A background process (started by the client) that exposes tools (like `fetch_pokemon_data`) via the Model Context Protocol. It interfaces directly with the MongoDB container.


## 🛠️ Tech Stack

* **Orchestration**: [LangGraph](https://www.langchain.com/langgraph) for stateful, multi-turn agent logic.
* **LLM Provider**: Ollama Cloud (via `ChatOpenAI` adapter) for high-parameter cloud models.
* **Database**: [MongoDB](https://www.mongodb.com/) for persistent Pokémon and Move data.
* **Tooling**: [FastMCP](https://github.com/jlowin/fastmcp) for rapid tool registration.
* **Monitoring**: [LangSmith](https://smith.langchain.com/) for full-trace observability.

## 📂 Project Structure

```text
├── client/                 # LangGraph Agent & Terminal UI
│   ├── app/
│   │   ├── core/           # Factory and MCP client logic
│   │   ├── services/       # Chat loop and state management
│   │   └── ui/             # Terminal formatting
│   └── main.py             # Client Entrypoint
├── server/                 # MCP Server (Tools)
│   ├── core/               # Logs, DB config, and App initialization
│   ├── logs/               # Persistent server logs
│   ├── tools/              # registered MCP tools
│   └── main.py             # Server Entrypoint
├── data/                   # MongoDB persistence & JSON seeds
├── infra/                  # Infrastructure scripts (Mongo init, etc.)
├── docker-compose.yml      # Service orchestration
└── Dockerfile              # Lean Python 3.11-slim environment
```

## 🚀 Getting Started

### 1. Prerequisites
* **Docker & Docker Compose** installed on your Ubuntu host.
* Valid API Keys for **Ollama Cloud** and **LangSmith**.

### 2. Configuration (`.env`)
Create a `.env` file in the root directory. **Note:** Do not use quotes around values.

```bash
LLM_PROVIDER=ollama_cloud
OLLAMA_CLOUD_API_KEY=your_api_key_here
OLLAMA_CLOUD_MODEL=qwen3-coder:480b-cloud
OLLAMA_CLOUD_BASE_URL=https://ollama.com/v1

MONGO_URL=mongodb://mongodb:27017/

LANGSMITH_TRACING_V2=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=pokedex-cli
```

### 3. Running the app
To ensure a smooth experience, the project includes a `run.sh` script to automate stack teardown, building, and interactive attachment.
```bash
./run.sh
```


## 📝 Key Implementation Details

### Database Networking
The MCP server connects to MongoDB using the internal Docker hostname `mongodb` instead of `localhost` to bridge the container gap.

### Persistence & Logging
* **MongoDB**: Data is persisted in `./data/db` on the host.
* **Logs**: Server logs are synced to `./server/logs/` via Docker volumes for real-time debugging on the Ubuntu host.

## 🛠️ Troubleshooting

* **Permission Denied (`data/db`)**: If the database fails to start, ensure the `data/` folder is in your `.dockerignore` to prevent Docker from trying to copy locked system files during build.
* **Connection Refused**: If the tool fails to reach MongoDB, verify that `MONGO_URL` in your code uses the service name `mongodb` rather than `127.0.0.1`.

---

**Bruno Lima** | Recife, Brazil