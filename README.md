# Activity Helper Agent 🤖

An intelligent AI agent that helps users discover and plan activities for their free time by leveraging various tools and APIs to provide personalized recommendations.

## 🌟 Features

- **Weather Integration**: Get activity suggestions based on current and forecasted weather conditions
- **Web Search**: Find relevant information about activities, events, and local attractions
- **Personalized Recommendations**: Receive suggestions based on user preferences and interests
- **Time-Aware Suggestions**: Get recommendations that fit your available time slots
- **Location-Based Activities**: Discover activities near your current location

## 🛠️ Tools & Integrations

- Weather API for real-time weather data
- Web search capabilities for up-to-date information
- Location services for nearby activity suggestions
- Calendar integration for time management
- User preference storage for personalized recommendations

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- API keys for required services
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/activity-helper-agent.git
cd activity-helper-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## 💻 Usage

```python
from activity_helper import ActivityAgent

agent = ActivityAgent()
suggestions = agent.get_activity_suggestions(
    location="San Francisco",
    time_available="2 hours",
    preferences=["outdoor", "active"]
)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all the open-source projects and APIs that make this possible
- Inspired by the need for better activity planning and discovery

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.
