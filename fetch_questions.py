import requests
import json

API_URL = "https://opentdb.com/api.php"

def fetch_questions(amount=5, category=18, difficulty='easy', timeout=5):
    url = f"{API_URL}?amount={amount}&category={category}&difficulty={difficulty}&type=multiple"
    try:
        response = requests.get(url, timeout=timeout)  # Added timeout parameter
        response.raise_for_status()
        data = response.json()
        if data["response_code"] == 0:
            # print("printing data",data)
            cache_questions(data["results"])
            return data["results"]
        else:
            print("API response code indicates no questions were returned.")
    except requests.exceptions.Timeout:
        print("Connection timed out. Please check your network or try again later.")
    except requests.RequestException as e:
        print(f"API error: {e}")
    return []

def cache_questions(questions, filename='questions_cache.json'):
    """Caches questions locally to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(questions, f)

def load_cached_questions(filename='questions_cache.json'):
    """Loads questions from the local cache file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No cached questions available.")
        return []
