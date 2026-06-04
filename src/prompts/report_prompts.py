# src/prompts/report_prompts.py
#
# PURPOSE: This file stores all the instructions (prompts) we send to the AI.
# Think of this as the "script" we hand to Gemini before asking it to work.
# Keeping prompts here makes them easy to find, edit, and improve.


def get_report_prompt(company_name: str, research_text: str) -> str:
    """
    Builds and returns the full prompt we send to Gemini.

    Why a function instead of just a variable?
    Because we need to INSERT the company name and research data
    into the prompt dynamically. A function lets us do that cleanly.

    Parameters:
        company_name  : The company the user typed (e.g. "Adani Realty")
        research_text : The formatted search results from search_tool.py

    Returns:
        A complete string prompt ready to be sent to Gemini.
    """

    # We use a triple-quoted string (""") so the prompt can span many lines
    # cleanly without needing \n everywhere.
    prompt = f"""
You are a senior business intelligence analyst specializing in Indian 
real estate and proptech sectors.

You have been asked to analyze a company called "{company_name}".

Below is fresh research data collected from the internet about this company:

=== RESEARCH DATA START ===
{research_text}
=== RESEARCH DATA END ===

Using this research, generate a structured intelligence report.

Your response must be a valid JSON object with EXACTLY these 5 keys.
Do not add any extra keys. Do not nest objects inside values.
All values must be plain strings.

Return ONLY the JSON. No explanation before it. No text after it.
Do not wrap it in markdown code fences.

{{
  "overview": "Write 3-4 sentences. Cover: what the company does, 
               which industry it operates in, its scale (revenue/size 
               if known), and its geographic presence. 
               Be factual and specific.",

  "business_info": "Write 2-3 paragraphs covering: major products or 
                    services offered, recent developments or news from 
                    2025-2026, any announced expansion plans, and any 
                    notable partnerships or achievements.",

  "challenges": "Identify exactly 3 business challenges specific to 
                 {company_name}. For each challenge: name it, explain 
                 why it exists for THIS company specifically, and what 
                 operational or financial impact it likely has. 
                 Do NOT write generic challenges like 'faces competition'. 
                 Base your reasoning on the research data provided.",

  "ai_opportunities": "Suggest exactly 3 AI-powered solutions tailored 
                       to {company_name}. For each suggestion include: 
                       (1) What the AI solution is, (2) Which specific 
                       challenge or gap it addresses, (3) How it would 
                       work in simple terms, (4) The expected business 
                       impact in measurable terms where possible. 
                       Examples of strong suggestions: AI-powered site 
                       selection using satellite + market data, NLP for 
                       automating RERA document compliance, lead scoring 
                       models for sales teams. Be this specific.",

  "pitch": "Write a one-page CEO pitch letter. Structure it as follows: 
            Paragraph 1 - Opening: Why you are reaching out. Reference 
            one specific challenge or opportunity you identified. 
            Paragraph 2 - What you found: Summarize your key research 
            findings about their business situation. 
            Paragraph 3 - What you recommend: Your 2-3 AI solutions and 
            their impact. 
            Paragraph 4 - Call to action: Request a 20-minute call. 
            Keep it professional, warm, and specific. 
            Do not use bullet points in the pitch. 
            Write as flowing paragraphs."
}}
"""
    # Return the complete prompt string
    return prompt


def format_research_for_prompt(research_data: dict) -> str:
    """
    Converts the raw search results dictionary from search_tool.py
    into a clean, readable text block that fits inside the prompt.

    Why a separate function?
    The raw search data is a nested dictionary with lots of structure.
    The AI reads plain text better than raw Python dictionaries.
    This function "flattens" that data into readable text.

    Parameters:
        research_data : The dictionary returned by search_company()

    Returns:
        A formatted string summarizing all search results.
    """

    formatted = ""

    # Loop through each search query and its results
    for query, results in research_data.items():

        # Add a section header for this query
        formatted += f"\n--- Topic: {query} ---\n"

        # If no results were found for this query
        if not results:
            formatted += "No results found for this topic.\n"
            continue

        # Loop through each individual search result
        for i, result in enumerate(results, start=1):

            title = result.get("title", "No title")
            content = result.get("content", "No content")
            url = result.get("url", "")

            # We limit content to 400 characters per result
            # Why? The full content would make the prompt too long
            # and expensive. 400 chars captures the key info.
            content_preview = content[:400]

            formatted += f"\nResult {i}: {title}\n"
            formatted += f"Summary: {content_preview}\n"
            formatted += f"Source: {url}\n"

    return formatted