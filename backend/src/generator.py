import json
import os

# Your exact categories
CATEGORIES = [
"LGBTQ"
]


def generate_batch():
    # Adjust path if necessary to find your countries.json
    with open('../data/countries.json', 'r') as f:
        countries = json.load(f)

    SYSTEM_PROMPT = (
    "You are a local cultural expert with deep, practical knowledge of global etiquette, legal nuances, and everyday customs.\n\n"
    "Provide exactly 2 sentences explaining the requested category norm for the target country.\n\n"
    "Guidelines:\n"
    "1. Sentence 1: State the actionable norm, legal rule, or practical expectation directly (e.g., specific tipping rates, tap water safety, dietary/meat norms, public behavior laws, exact PDA thresholds).\n"
    "2. Sentence 2: Provide the local rationale, cultural etiquette context, or specific operational detail (e.g., squat vs. Western toilets, payment methods, local sanctions).\n"
    "3. Category Specifics: Address the exact topic requested without shifting focus to general safety or general travel tips.\n"
    "4. Content Quality: Avoid generic filler (e.g., 'be respectful,' 'exercise caution,' 'do research,' or 'check local laws'). Be direct and factual.\n"
    "5. Constraints: Output only the 2-sentence insight. Do not include introductory text, conversational filler, or Markdown formatting."
    )
    RESPONSE_FORMAT = {
        "type": "json_schema",
        "json_schema": {
            "name": "cultural_norm_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "insight": {
                        "type": "string",
                        "description": "Exactly two sentences detailing the cultural norm."
                    }
                },
                "required": ["insight"],
                "additionalProperties": False
            }
        }
    }

    with open('../data/batch_input.jsonl', 'w', encoding='utf-8') as f:
        for category in CATEGORIES:
            for country in countries:
                custom_id = f"{category}:{country}"

                payload = {
                    "custom_id": custom_id,
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": "gpt-4o-mini",
                        "temperature": 0.2,
                        "max_tokens": 120,  # Increased slightly so JSON envelope + content never truncates mid-sentence
                        "response_format": RESPONSE_FORMAT,
                        "messages": [
                            {
                                "role": "system",
                                "content": SYSTEM_PROMPT
                            },
                            {
                                "role": "user",
                                "content": f"What is the cultural norm for '{category}' in {country}?"
                            }
                        ]
                    }
                }
                f.write(json.dumps(payload, ensure_ascii=False) + '\n')

    print(f"Generated {len(CATEGORIES) * len(countries)} requests in data/batch_input.jsonl")


if __name__ == "__main__":
    generate_batch()