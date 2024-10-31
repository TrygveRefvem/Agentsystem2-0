# Agentsystem 2.0

A dynamic multi-agent system that provides specialized analysis and responses based on user queries. The system automatically selects relevant expert agents based on query content and facilitates a structured dialogue between them.

## Core Features

- Dynamic agent selection based on query analysis
- Real-time agent interaction and dialogue
- Consensus building among multiple agents
- WebSocket-based communication
- Tailwind CSS for styling

## Technical Stack

- Backend: FastAPI, Python 3.11
- Frontend: HTML, JavaScript, Tailwind CSS
- AI: Azure OpenAI API (GPT-4)
- Container: Docker
- WebSocket for real-time communication

## Project Structure
Agentsystem2-0/
├── app/
│   ├── api/
│   │   ├── routes.py         # API endpoints
│   │   └── websocket.py      # WebSocket handling
│   ├── core/
│   │   ├── config.py         # Configuration settings
│   │   └── logging.py        # Logging setup
│   ├── agents/
│   │   ├── base.py          # Base agent class
│   │   └── selector.py      # Agent selection logic
│   ├── services/
│   │   ├── openai.py        # OpenAI integration
│   │   └── dialogue.py      # Dialogue management
│   ├── templates/
│   │   └── index.html       # Main frontend
│   └── static/
│       ├── css/
│       └── js/modules/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/TrygveRefvem/Agentsystem2-0.git
cd Agentsystem2-0
cat > .env << 'EOL'
AZURE_OPENAI_ENDPOINT="your_endpoint"
AZURE_OPENAI_API_KEY="your_key"
AZURE_OPENAI_DEPLOYMENT="your_deployment"
LOG_LEVEL=INFO
ENV=development
EOL
docker build -t agentsystem2-0 .
docker run -p 8000:8000 \
  -e AZURE_OPENAI_ENDPOINT="your_endpoint" \
  -e AZURE_OPENAI_API_KEY="your_key" \
  -e AZURE_OPENAI_DEPLOYMENT="your_deployment" \
  agentsystem2-0
docker-compose up --build
Current Functionality

Question Analysis: System analyzes user queries to understand the context and requirements
Dynamic Agent Selection: Automatically selects 2-4 relevant expert agents based on the query
Interactive Dialogue: Agents engage in structured dialogue, building on each other's insights
Consensus Building: System generates a final consensus from agent discussions
Real-time Updates: Frontend updates in real-time as agents respond

Development State
Current working version includes:

Basic agent system with dynamic selection
WebSocket communication
Frontend interface with Tailwind CSS styling
Docker containerization
Environment variable configuration

Known Limitations

Maximum of 4 agents per dialogue
Responses limited to 2-3 sentences per agent
Currently optimized for Norwegian language queries

Future Improvements
Planned enhancements:

Enhanced agent specialization
Improved consensus algorithms
Better error handling
More detailed agent interactions
Extended language support

Contributing

Create a new branch for features:

bashCopygit checkout -b feature/your-feature-name

Make changes and commit:

bashCopygit add .
git commit -m "Description of changes"

Push changes:

bashCopygit push origin feature/your-feature-name

Create a Pull Request on GitHub

Version History

v2.0.0: Initial working version with dynamic agents and WebSocket communication

Environment Variables
Required environment variables:

AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT
LOG_LEVEL (optional, defaults to INFO)
ENV (optional, defaults to development)

License
MIT License
Contact
Trygve Refvem - GitHub Profile
