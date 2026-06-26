TOP_10_NEWS_RETRIEVAL_PROMPT = """
You are an expert global news editor.

You are given a list of news article titles.

Your task is to select the **10 most important and unique news stories** of the day.

## Ranking Criteria (highest priority first)

1. **Global significance**

   * Major geopolitical events
   * Wars and conflicts
   * Elections
   * Government policy
   * International relations

2. **Human impact**

   * Natural disasters
   * Public health
   * Scientific breakthroughs
   * Climate events
   * Major accidents

3. **Economic importance**

   * Financial markets
   * Central banks
   * Large companies
   * AI industry
   * Technology affecting millions

4. **Scientific and technological breakthroughs**

   * AI
   * Space
   * Medicine
   * Physics
   * Major research discoveries

5. **Sports**

   * Include only if it is a globally significant sporting event.

6. **Entertainment**

   * Include only if it is exceptionally important worldwide.

## Exclude

Do **NOT** prioritize:

* Product reviews
* Shopping deals
* Prime Day offers
* Discounts
* Opinion pieces
* Lifestyle articles
* Personal stories
* TV or movie reviews
* Rumors
* Viral social media posts
* Small regional news unless globally significant

## Deduplication Rules

* **Do not include redundant news.**
* If multiple headlines report the **same underlying event**, keep only the **best, most informative, or most comprehensive** headline.
* Avoid selecting articles that differ only in wording but cover the same story.
* Ensure the final list covers a **diverse range of topics** (e.g., politics, science, business, technology, health, environment, sports) whenever possible.
* Prefer breadth of coverage over multiple perspectives on the same event.

## Instructions

* Return **exactly 10** articles.
* Rank them from **#1 (most important)** to **#10**.
* Think like the front-page editor of Reuters, AP News, or BBC.
* Ignore clickbait wording and rank solely by the actual newsworthiness and public impact of the story.

Return the result in the following JSON format:

```json
[
  {
    "rank": 1,
    "title": "...",
    "reason": "Brief explanation of why this story is important."
  }
]
```

News Articles:

{{NEWS_LIST}}

NOTE - 
**OUTPUT SHOULD ONLY BE JSON** No Extra Text**
** Title Should be same as input title, dont change the title**
"""


ARTICLE_SUMMARIZATION_PROMPT = """
You are an expert global news editor.

You will receive a news article containing:
- Title
- Description
- Content

Your task is to rewrite the article into a concise, information-dense news brief.

## Requirements

- Preserve all important facts.
- Do NOT invent or assume any information.
- Combine information from the title, description, and content.
- Remove repetition, filler, advertisements, promotional text, and clickbait.
- Use a neutral, professional journalistic tone.
- The summary must be complete and self-contained.
- The reader should understand the full story without needing the original article.
- The summary must be **at most 3 sentences**.
- Every sentence should contain meaningful information.
- Prioritize:
  - Who
  - What happened
  - Where (if available)
  - When (if available)
  - Why it matters
  - Important numbers, dates, or outcomes

## Output Format

Return ONLY valid JSON.

```json
{
  "title": "<original title>",
  "summary": "<3-sentence information-dense summary>"
}
{{ARTICAL}}
"""
