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
    "Recycling", "Toilets", "Money Talk", "Meat", "Inclusivity", "Public Behavior"
]

# Sample List (In production, load from countries.json)
COUNTRIES = ["Japan", "Brazil", "Egypt", "France", "Thailand", "Germany", "Mexico", "India", "Italy", "Morocco"]


def test_single_entry():
    country = random.choice(COUNTRIES)
    country = "Egypt"
    category = random.choice(CATEGORIES)
    # category = "Alcohol"

    print(f"--- Testing: {category} in {country} ---")

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        temperature=0.2,  # Low temperature ensures adherence to rules and factual consistency
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a local cultural expert with deep, practical knowledge of global etiquette, legal nuances, and everyday customs.\n\n"
                    "Provide exactly 2 sentences explaining the requested category norm for the target country.\n\n"
                    "Guidelines:\n"
                    "1. Sentence 1: State the actionable norm, legal rule, or practical expectation directly (e.g., specific tipping rates, tap water safety, dietary/meat norms, public behavior laws, exact PDA thresholds).\n"
                    "2. Sentence 2: Provide the local rationale, cultural etiquette context, or specific operational detail (e.g., squat vs. Western toilets, payment methods, local sanctions).\n"
                    "3. Category Specifics: Address the exact topic requested without shifting focus to general safety or general travel tips.\n"
                    "4. Content Quality: Avoid generic filler (e.g., 'be respectful,' 'exercise caution,' 'do research,' or 'check local laws'). Be direct and factual.\n"
                    "5. Constraints: Output only the 2-sentence insight. Do not include introductory text, conversational filler, or Markdown formatting."
                ),
            },
            {
                "role": "user",
                "content": f"What is the cultural norm for '{category}' in {country}?",
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "cultural_norm_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "insight": {
                            "type": "string",
                            "description": "Exactly two sentences detailing the cultural norm.",
                        }
                    },
                    "required": ["insight"],
                    "additionalProperties": False,
                },
            },
        },
    )

    result = response.choices[0].message.content
    print(response.model_dump_json())
    print(f"Result: {result}")
    return result


if __name__ == "__main__":
    test_single_entry()
