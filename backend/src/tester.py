import random

from dotenv import load_dotenv
from openai import OpenAI

# from processor import process_results

load_dotenv()
client = OpenAI()

# Your Categories
CATEGORIES = [
    "Etiquette", "Clothing", "Alcohol", "Safety", "Tipping", "Dining",
    "Punctuality", "Religion", "Taboos", "Nature", "Greetings",
    "Personal Space", "Eye Contact", "Swearing", "Titles & Address",
    "Gift Giving", "Gender Norms", "Noise Levels", "Physical Touch",
    "Social Hierarchy", "Bargaining", "Photography", "Transportation",
    "Queueing", "Coffee & Tea", "Bill Paying", "Street Food", "Smoking",
    "Drinking Water", "Sustainability", "Relationships", "PDA", "Tattoos",
    "Recycling", "Toilets", "Money Talk"
]

# Sample List (In production, load from countries.json)
COUNTRIES = ["Japan", "Brazil", "Egypt", "France", "Thailand", "Germany", "Mexico", "India", "Italy", "Morocco"]


def test_single_entry():
    country = random.choice(COUNTRIES)
    country = "Egypt"
    category = random.choice(CATEGORIES)
    # category = "Alcohol"

    print(f"--- Testing: {category} in {country} ---")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a world-class travel cultural expert. Provide a concise, 2-sentence insight about the specific cultural norm requested. Show nuance in your response, try not to be to general and if there are exceptions to a rule, show them. Be factual. Do not speak too much, keep it under 20 words."},
            {"role": "user", "content": f"What is the cultural norm for '{category}' in {country}?"}
        ]
    )

    result = response.choices[0].message.content
    print(response.model_dump_json())
    print(f"Result: {result}")
    return result


if __name__ == "__main__":
    test_single_entry()
