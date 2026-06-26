import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class JokeGenerator:
    """Handles random joke generation from external APIs"""
    
    # Multiple joke APIs for fallback support
    JOKE_APIS = {
        "official": "https://official-joke-api.appspot.com/random_joke",
        "jokeapi": "https://v2.jokeapi.dev/joke/Any?format=json",
        "dadjoke": "https://icanhazdadjoke.com/?format=json"
    }
    
    @staticmethod
    def get_random_joke() -> Optional[Dict]:
        """
        Fetch a random joke from an external API with fallback support
        
        Returns:
            Dict with 'joke' and 'type' keys, or None if all APIs fail
        """
        # Try Official Joke API first
        try:
            response = requests.get(JokeGenerator.JOKE_APIS["official"], timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "joke": f"{data['setup']}\n\n{data['punchline']}",
                    "type": "setup-punchline",
                    "category": data.get('type', 'general')
                }
        except Exception as e:
            logger.warning(f"Official Joke API failed: {e}")
        
        # Try JokeAPI as fallback
        try:
            response = requests.get(JokeGenerator.JOKE_APIS["jokeapi"], timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('type') == 'twopart':
                    joke_text = f"{data['setup']}\n\n{data['delivery']}"
                else:
                    joke_text = data.get('joke', 'No joke available')
                
                return {
                    "joke": joke_text,
                    "type": data.get('type', 'single'),
                    "category": data.get('category', 'general')
                }
        except Exception as e:
            logger.warning(f"JokeAPI failed: {e}")
        
        # Try Dad Jokes API as final fallback
        try:
            response = requests.get(JokeGenerator.JOKE_APIS["dadjoke"], timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "joke": data.get('joke', 'No joke available'),
                    "type": "dad-joke",
                    "category": "dad-jokes"
                }
        except Exception as e:
            logger.warning(f"Dad Jokes API failed: {e}")
        
        # If all APIs fail, return a built-in joke
        logger.error("All joke APIs failed, returning built-in joke")
        return JokeGenerator.get_builtin_joke()
    
    @staticmethod
    def get_builtin_joke() -> Dict:
        """Return a built-in joke as fallback"""
        builtin_jokes = [
            {
                "joke": "Why don't scientists trust atoms?\n\nBecause they make up everything!",
                "type": "setup-punchline",
                "category": "programming"
            },
            {
                "joke": "Why did the programmer quit his job?\n\nBecause he didn't get arrays.",
                "type": "setup-punchline",
                "category": "programming"
            },
            {
                "joke": "How many programmers does it take to change a light bulb?\n\nNone, that's a hardware problem!",
                "type": "setup-punchline",
                "category": "programming"
            },
            {
                "joke": "Why do Java developers wear glasses?\n\nBecause they don't C#",
                "type": "setup-punchline",
                "category": "programming"
            }
        ]
        import random
        return random.choice(builtin_jokes)
    
    @staticmethod
    def format_joke(joke_data: Dict) -> str:
        """Format joke data for display"""
        if not joke_data:
            return "❌ Could not fetch a joke at this time. Try again later!"
        
        category_emoji = {
            "general": "😄",
            "programming": "👨‍💻",
            "knock-knock": "🚪",
            "dad-jokes": "👨",
            "dark": "🖤",
            "pun": "🎭"
        }
        
        emoji = category_emoji.get(joke_data.get('category', 'general'), '😂')
        
        return f"""{emoji} <b>{joke_data.get('category', 'GENERAL').upper()}</b>

{joke_data.get('joke', 'No joke available')}"""
