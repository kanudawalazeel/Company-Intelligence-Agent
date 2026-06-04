# src/agents/analyst.py
import os
import json
from dotenv import load_dotenv
from groq import Groq

from src.prompts.report_prompts import get_report_prompt, format_research_for_prompt

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_report(company_name: str, research_data: dict) -> dict:
    """
    Takes company name + search results.
    Returns structured 5-section report as a dictionary.
    """

    research_text = format_research_for_prompt(research_data)
    prompt = get_report_prompt(company_name, research_text)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Free, very capable model
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior business intelligence analyst. Always respond with valid JSON only. No extra text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000,
        )

        raw_text = response.choices[0].message.content.strip()

        # Clean markdown fences if present
        if "```" in raw_text:
            parts = raw_text.split("```")
            raw_text = parts[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()

        report = json.loads(raw_text)
        return report

    except json.JSONDecodeError as e:
        print(f"⚠️  JSON parsing failed: {e}")
        return _error_report("Could not parse AI response as JSON.")

    except Exception as e:
        print(f"⚠️  Groq API error: {e}")
        return _error_report(str(e))


def _error_report(message: str) -> dict:
    return {
        "overview": f"Error: {message}",
        "business_info": "Report generation failed. Please try again.",
        "challenges": "Report generation failed. Please try again.",
        "ai_opportunities": "Report generation failed. Please try again.",
        "pitch": "Report generation failed. Please try again."
    }


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    ))

    from src.tools.search_tool import search_company

    test_company = "Sobha Limited"
    print(f"🔍 Searching for: {test_company}")
    research = search_company(test_company)
    print("✅ Search complete. Generating report...")

    report = generate_report(test_company, research)

    print("\n✅ Report generated!\n")
    for section, content in report.items():
        print(f"{'='*50}")
        print(f"  {section.upper()}")
        print(f"{'='*50}")
        print(content[:400])
        print()