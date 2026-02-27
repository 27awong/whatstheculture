import json
import os

# Your exact categories
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


def generate_batch():
    # Adjust path if necessary to find your countries.json
    with open('../data/countries.json', 'r') as f:
        countries = json.load(f)

    with open('../data/batch_input.jsonl', 'w', encoding='utf-8') as f:
        for category in CATEGORIES:
            for country in countries:
                # NEW ID FORMAT: "CultureName:CountryName"
                # This matches your new JS contentMap key requirements
                custom_id = f"{category}:{country}"

                payload = {
                    "custom_id": custom_id,
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a world-class travel cultural expert. Provide a concise, 2-sentence insight about the specific cultural norm requested. Be factual and avoid generic travel advice. Do not speak too much, keep it under 20 words."
                            },
                            {
                                "role": "user",
                                "content": f"What is the cultural norm for {category} in {country}?"
                            }
                        ],
                        "max_tokens": 45
                    }
                }
                f.write(json.dumps(payload, ensure_ascii=False) + '\n')

    print(f"Generated {len(CATEGORIES) * len(countries)} requests in data/batch_input.jsonl")


if __name__ == "__main__":
    generate_batch()