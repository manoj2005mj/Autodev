# 🤖 AutoDev: AI Software Architect

An agentic system powered by Google Gemini that automatically generates full-stack web applications from user stories.

## Features

- **📋 Architecture Agent**: Designs API specs and system architecture
- **🎨 Frontend Agent**: Generates React TypeScript code
- **⚙️ Backend Agent**: Generates FastAPI Python code  
- **🔍 Reflector Agent**: Analyzes errors and plans fixes
- **💬 Human Loop**: Interactive feedback and code refinement
- **📁 JSON Export**: All generated code saved to JSON format
- **🐳 Docker Support**: Full Docker and Docker Compose setup

## Quick Start

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/manoj2005mj/Autodev.git
   cd Autodev/code_gen_agent
   ```

2. **Set up environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API key:**
   Create a `.env` file in `code_gen_agent/` directory:
   ```bash
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Run locally:**
   ```bash
   streamlit run streamlit_app.py
   ```
   Access at: `http://localhost:8501`

### Docker Setup

#### Option 1: Docker Compose (Recommended)

```bash
cd code_gen_agent
docker-compose up
```

Access at: `http://localhost:8501`

#### Option 2: Docker CLI

1. **Build the image:**
   ```bash
   cd code_gen_agent
   docker build -t autodev:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     -p 8501:8501 \
     -e GOOGLE_API_KEY=your_api_key_here \
     -v $(pwd)/output:/app/output \
     --name autodev \
     autodev:latest
   ```

3. **Check logs:**
   ```bash
   docker logs -f autodev
   ```

## Project Structure

```
code_gen_agent/
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── architect.py     # Architecture & API design
│   │   ├── frontend.py      # React code generation
│   │   ├── backend.py       # FastAPI code generation
│   │   ├── human.py         # Human feedback node
│   │   ├── reflector.py     # Error analysis & routing
│   │   └── router.py        # Decision routing logic
│   ├── core/
│   │   ├── graph.py         # LangGraph workflow
│   │   └── state.py         # State management
│   ├── utils/
│   │   ├── llm_helper.py    # Gemini integration
│   │   └── code_exporter.py # JSON export utility
│   └── prompts/
│       └── system_prompts.py # Agent prompts
├── tests/
│   └── test_graph.py        # Basic tests
├── output/                  # Generated code exports (JSON)
├── streamlit_app.py         # Streamlit web interface
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image config
├── docker-compose.yml       # Docker Compose config
└── README.md               # This file
```

## Usage

### Web Interface (Streamlit)

1. **Enter a User Story** in the sidebar:
   ```
   "Build a task management app with user authentication, 
    real-time notifications, and a modern dark UI."
   ```

2. **Click "Start New Project"** — watch the architecture, frontend, and backend code generate

3. **Review the generated code** in the tabs

4. **Provide feedback** (or type "success" to finish):
   - Report errors found when running the code
   - Request specific changes or improvements
   - The reflector analyzes feedback and agents iterate

### Command Line (Python)

```bash
cd code_gen_agent
python src/main.py
```

## Generated Output

All generated code is automatically exported to `output/` as JSON files with metadata:

```json
{
  "agent": "frontend",
  "timestamp": "2025-12-11T14:30:45.123456",
  "metadata": {
    "user_story": "Build a To-Do List app...",
    "iteration": 0,
    "mode": "generation"
  },
  "files": {
    "App.tsx": "import React from ...",
    "index.tsx": "ReactDOM.createRoot(...)"
  },
  "file_count": 2
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | ✅ Yes | Your Gemini API key from Google AI Studio |
| `PYTHONUNBUFFERED` | ❌ No | Set to `1` for unbuffered output |
| `STREAMLIT_SERVER_PORT` | ❌ No | Streamlit port (default: 8501) |

## API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Store it securely (e.g., in `.env` file)
4. Never commit secrets to version control

## Docker Troubleshooting

### Container exits immediately
```bash
docker logs autodev
# Check for missing GOOGLE_API_KEY or other errors
```

### Port already in use
```bash
# Use a different port
docker run -p 9000:8501 autodev:latest
```

### Clear Docker cache
```bash
docker-compose down --volumes
docker system prune -a
docker-compose up --build
```

## Development

### Running Tests

```bash
pip install pytest
pytest -q
```

### Code Format & Linting

```bash
pip install black flake8
black src/
flake8 src/
```

## Architecture

The system uses **LangGraph** with a state machine workflow:

```
User Story → Architect → Frontend/Backend (parallel)
                ↓
           Human Review
                ↓
           Reflector (analyze errors)
                ↓
         Router (decide next agent)
                ↓
    [Repeat or End]
```

## Technologies

- **LLM**: Google Gemini 2.5 Flash
- **Framework**: LangGraph, LangChain
- **Web UI**: Streamlit
- **Languages**: Python, React/TypeScript, FastAPI
- **Containerization**: Docker, Docker Compose

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Push and open a pull request

## License

MIT License — see LICENSE file for details

## Support

For issues or questions:
- GitHub Issues: [manoj2005mj/Autodev](https://github.com/manoj2005mj/Autodev/issues)
- Documentation: Check the README and inline code comments
