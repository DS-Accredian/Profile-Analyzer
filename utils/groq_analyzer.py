import json
import os
import requests

def analyze_report_with_groq(report_text):
    """Sends the raw report and prompt manifest to Groq using Llama 3.1"""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "prompt_library.json")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            prompt_library = json.load(file)
    except Exception:
        prompt_library = []

    # Create a lightweight manifest
    manifest = [{"id": p.get("id"), "title": p.get("title"), "purpose": p.get("description")} for p in prompt_library]
    manifest_json = json.dumps(manifest, indent=2)

    # NEW SCHEMA: Instruct Llama to dynamically extract ALL critical gaps (1 to 6+)
    system_prompt = f"""You are a Strategic LinkedIn Profile Analyst and Routing Engine.
Your job is to read the raw AI Profile Audit Report provided by the user, and map their critical gaps to the exact solutions in our Prompt Library.

Here is our Prompt Library Manifest:
{manifest_json}

You MUST output ONLY a raw JSON object with the exact following schema:
{{
  "executive_summary": "A 2-3 sentence professional summary of their overall profile state.",
  "parsed_health_score": 85, 
  "strategic_gaps": [
    {{
      "gap_name": "Short title of the gap (e.g., Weak Headline)",
      "explanation": "1-sentence explanation of why it is failing.",
      "option_1_id": Integer matching the best prompt ID from the manifest,
      "option_2_id": Integer matching the second best prompt ID alternative
    }}
  ]
}}
Note: Provide ALL critical strategic gaps found in the report (typically between 1 and 6 gaps). Do not force exactly 3. If the profile has 5 major issues, list all 5. If it only has 1 or 2, just list those.
"""

    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return {"error": "GROQ_API_KEY environment variable is not set."}

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the raw report to analyze:\n\n{report_text}"}
        ],
        "temperature": 0.2, 
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() 
        
        response_data = response.json()
        response_content = response_data["choices"][0]["message"]["content"]
        
        parsed_json = json.loads(response_content)
        return parsed_json
        
    except requests.exceptions.RequestException as e:
        error_msg = f"API Request failed: {str(e)}"
        if 'response' in locals() and hasattr(response, 'text'):
            error_msg += f" - Response: {response.text}"
        return {"error": error_msg}
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON from Groq: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}




# import json
# import os
# import requests

# def analyze_report_with_groq(report_text):
#     """Sends the raw report and prompt manifest to Groq using Llama 3.1"""
    
#     # 1. Load the prompt library to create the manifest
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(current_dir, "prompt_library.json")
    
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             prompt_library = json.load(file)
#     except Exception:
#         prompt_library = []

#     # 2. Create a lightweight manifest (ID, Title, Description)
#     manifest = [{"id": p.get("id"), "title": p.get("title"), "purpose": p.get("description")} for p in prompt_library]
#     manifest_json = json.dumps(manifest, indent=2)

#     # 3. Build the highly structured System Prompt
#     system_prompt = f"""You are a Strategic LinkedIn Profile Analyst and Routing Engine.
# Your job is to read the raw AI Profile Audit Report provided by the user, and map their critical gaps to the exact solutions in our Prompt Library.

# Here is our Prompt Library Manifest:
# {manifest_json}

# You MUST output ONLY a raw JSON object with the exact following schema:
# {{
#   "executive_summary": "A 2-3 sentence professional summary of their overall profile state.",
#   "parsed_health_score": 85, 
#   "top_gaps_explained": [
#     "Clear explanation of gap 1",
#     "Clear explanation of gap 2",
#     "Clear explanation of gap 3"
#   ],
#   "recommended_prompt_ids": [Array of 3 to 5 integers matching the exact IDs from the manifest that solve these gaps]
# }}
# """

#     # 4. Execute API Call using requests (Matching your Colab logic)
#     api_key = os.environ.get("GROQ_API_KEY", "")
#     if not api_key:
#         return {"error": "GROQ_API_KEY environment variable is not set. Please run: export GROQ_API_KEY='your_key'"}

#     url = "https://api.groq.com/openai/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": "llama-3.1-8b-instant",
#         "messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": f"Here is the raw report to analyze:\n\n{report_text}"}
#         ],
#         "temperature": 0.2, # Lower temperature forces the AI to be highly logical/deterministic
#         "response_format": {"type": "json_object"} # Forces perfect JSON output
#     }

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status() # Instantly flags if there is a 401 Unauthorized or 404 Model Not Found
        
#         response_data = response.json()
#         response_content = response_data["choices"][0]["message"]["content"]
        
#         # Parse the JSON string returned by Llama into a Python Dictionary
#         parsed_json = json.loads(response_content)
#         return parsed_json
        
#     except requests.exceptions.RequestException as e:
#         error_msg = f"API Request failed: {str(e)}"
#         if 'response' in locals() and hasattr(response, 'text'):
#             error_msg += f" - Response: {response.text}"
#         return {"error": error_msg}
#     except json.JSONDecodeError as e:
#         return {"error": f"Failed to parse JSON from Groq: {str(e)}"}
#     except Exception as e:
#         return {"error": str(e)}
