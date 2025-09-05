import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import RateLimitError

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def review_function(code: str, docstring: str = "") -> str:
    """
    Send a Python function to the OpenAI API for review.
    Returns AI feedback as a string.
    """

    # 1. Build the prompt
    prompt = f"""
You are a senior software engineer. Review the following Python function.
Focus on:
- Correctness
- Readability
- Efficiency
- Best practices
- Edge cases

Function source code:
```python
{code}
"""
    # 2. Build messages properly
    messages = [
        {"role": "system", "content": "You are a senior Python engineer."},
        {"role": "user", "content": prompt}
    ]

    try:
        # 3. Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # cheaper, lighter, still works
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()

    except RateLimitError:
        # fallback to mock response if quota exhausted
        return "⚠️ Quota exceeded. (Mock review: function looks okay, but handle edge cases)."

if __name__ == "__main__":
    sample_code = """
def add(a, b):
    return a+b
"""
    print(review_function(sample_code))
