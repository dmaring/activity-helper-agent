import os
from typing import List, Dict, Optional
from openai import OpenAI
import json
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ActivityHelperAgent:
    def __init__(self):
        """Initialize the Activity Helper Agent with OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.assistant = self._create_assistant()
        self.thread = self.client.beta.threads.create()

    def _create_assistant(self):
        """Create and configure the OpenAI assistant with tools."""
        return self.client.beta.assistants.create(
            name="Activity Helper",
            instructions="""You are an AI assistant that helps users find and plan activities for their free time.
            You can check weather, search for activities, and provide personalized recommendations.
            Always consider the user's preferences, available time, and current conditions when making suggestions.""",
            model="gpt-4-turbo-preview",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get current weather conditions for a location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "City name or coordinates"
                                }
                            },
                            "required": ["location"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "search_activities",
                        "description": "Search for activities based on preferences and location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query for activities"
                                },
                                "location": {
                                    "type": "string",
                                    "description": "Location to search in"
                                }
                            },
                            "required": ["query", "location"]
                        }
                    }
                }
            ]
        )

    def get_weather(self, location: str) -> Dict:
        """Get weather information for a location using OpenWeatherMap API."""
        api_key = os.getenv("OPENWEATHER_API_KEY")
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch weather data"}

    def search_activities(self, query: str, location: str) -> List[Dict]:
        """Search for activities using a search API (placeholder implementation)."""
        # This is a placeholder implementation
        # In a real application, you would integrate with a proper activities API
        return [
            {
                "name": "Sample Activity",
                "description": f"Activity related to {query} in {location}",
                "duration": "2 hours",
                "cost": "Free"
            }
        ]

    def get_activity_suggestions(
        self,
        location: str,
        time_available: str,
        preferences: List[str]
    ) -> Dict:
        """Get personalized activity suggestions based on user input."""
        # Create a message with the user's request
        message = f"""Please suggest activities for:
        Location: {location}
        Time Available: {time_available}
        Preferences: {', '.join(preferences)}
        """

        # Add the message to the thread
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )

        # Wait for the run to complete and handle tool calls
        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )
            
            if run_status.status == "completed":
                break
            elif run_status.status == "requires_action":
                tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []
                
                for tool_call in tool_calls:
                    result = None
                    if tool_call.function.name == "get_weather":
                        result = self.get_weather(
                            json.loads(tool_call.function.arguments)["location"]
                        )
                    elif tool_call.function.name == "search_activities":
                        args = json.loads(tool_call.function.arguments)
                        result = self.search_activities(
                            args["query"],
                            args["location"]
                        )
                    
                    if result is not None:
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(result)
                        })

                # Submit tool outputs
                self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

        # Get the final response
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        
        # Return the latest assistant message
        for message in messages.data:
            if message.role == "assistant":
                return {
                    "suggestions": message.content[0].text.value,
                    "timestamp": datetime.now().isoformat()
                }

        return {"error": "No suggestions generated"}

# Example usage
if __name__ == "__main__":
    agent = ActivityHelperAgent()
    suggestions = agent.get_activity_suggestions(
        location="San Francisco",
        time_available="2 hours",
        preferences=["outdoor", "active"]
    )
    print(json.dumps(suggestions, indent=2)) 