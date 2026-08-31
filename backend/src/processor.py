import json
import re

def process_results(input_file_path):
    """
    Reads the Batch API output, extracts the clean string from the response 
    (removing any {"insight": "..."} JSON wrappers), and maps custom_id to contentMap.json.
    """
    content_map = {}
    
    # 1. Verification Pass
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                response = json.loads(line)
                if response.get('response') and response['response'].get('status_code') == 200:
                    finish_reason = response["response"]["body"]["choices"][0]["finish_reason"]
                    if finish_reason != "stop":
                        print(f"Warning: Unexpected finish_reason '{finish_reason}' for key {response.get('custom_id')}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
        return
    except KeyError as e:
        print(f"KeyError encountered during verification: {e}")

    # 2. Main Processing Pass
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue

                data = json.loads(line)
                key = data.get('custom_id')

                if data.get('response') and data['response'].get('status_code') == 200:
                    raw_content = data['response']['body']['choices'][0]['message']['content'].strip()
                    
                    # Extract the pure string if structured inside a JSON object: {"insight": "..."}
                    clean_text = raw_content
                    try:
                        parsed_json = json.loads(raw_content)
                        if isinstance(parsed_json, dict) and "insight" in parsed_json:
                            clean_text = parsed_json["insight"]
                    except json.JSONDecodeError:
                        # Fallback regex cleanup if the JSON was malformed/escaped as raw text
                        clean_text = re.sub(r'^\s*\{\s*"insight"\s*:\s*"(.*)"\s*\}\s*$', r'\1', raw_content, flags=re.DOTALL)
                        clean_text = clean_text.replace('\\"', '"')

                    content_map[key] = clean_text.strip()
                else:
                    print(f"Error or missing data in request: {key}")

        # Write output file
        with open("contentMap.json", "w", encoding='utf-8') as f:
            json.dump(content_map, f, indent=2, ensure_ascii=False)

        print(f"Successfully generated contentMap.json with {len(content_map)} entries.")

    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")


if __name__ == "__main__":
    process_results("../data/batch_output.jsonl")