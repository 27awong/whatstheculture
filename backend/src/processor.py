import json


def process_results(input_file_path):
    """
    Reads the Batch API output and maps the human-readable
    custom_id (Culture:Country) to the generated content.
    """
    content_map = {}

    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue

                data = json.loads(line)

                # The custom_id is now "Culture:Country" (e.g., "Etiquette:Japan")
                # This matches your new JavaScript logic perfectly.
                key = data.get('custom_id')

                # Check if the API request was successful
                if data.get('response') and data['response'].get('status_code') == 200:
                    content = data['response']['body']['choices'][0]['message']['content'].strip()
                    content_map[key] = content
                else:
                    print(f"Error or missing data in request: {key}")

        # Write the final map to JSON
        with open("contentMap.json", "w", encoding='utf-8') as f:
            json.dump(content_map, f, indent=2, ensure_ascii=False)

        print(f"Successfully generated contentMap.json with {len(content_map)} entries.")

    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")


if __name__ == "__main__":
    # Point this to the file you download from the OpenAI Batch dashboard
    process_results("../data/batch_output.jsonl")