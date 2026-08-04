import json
import re

from app.evaluation.groq_eval import generate_response
from app.evaluation.prompt_templates import build_prompt


# ============================================================
# Hallucination Detection Agent
# ============================================================

def evaluate_hallucination(question, ai_response, reference):
    """
    Detects unsupported or hallucinated claims in the AI response.
    """

    evaluation_task = """
Evaluate ONLY hallucinations in the AI response.

Compare the AI response with the reference answer or retrieved context.

Determine whether the AI has added information that is NOT supported by the reference.

Scoring Rubric:

10 = No hallucinations. Every statement is fully supported.

8-9 = Very minor unsupported details.

6-7 = Mostly supported with one small unsupported claim.

4-5 = Several unsupported claims.

2-3 = Mostly hallucinated.

1 = Almost entirely hallucinated.

0 = Completely fabricated information.

Evaluation Rules:

• Evaluate ONLY hallucinations.
• Ignore grammar.
• Ignore completeness.
• Ignore writing style.
• Ignore relevance.
• Ignore whether the answer is long or short.
• Penalize only unsupported or invented facts.
• Give 10 only when every important statement is supported.
• Give 0 only when almost everything is fabricated.
• If the AI response matches the reference answer exactly, the hallucination score MUST be 10.
• If every claim in the AI response is supported by the reference, the score MUST be 10.
• Give a score of 0 ONLY when the response is almost entirely fabricated or unsupported.
• Ensure that the score is consistent with the reason.

IMPORTANT:

Return ONLY valid JSON.

Do NOT use markdown.

Do NOT use ```json.

Do NOT write any explanation outside JSON.

Expected format:

{
    "score": <0-10>,
    "reason": "<brief explanation>",
    "evidence": "<unsupported or supported statements>",
    "status": "<PASS or FAIL>"
}
"""

    prompt = build_prompt(
        question=question,
        ai_response=ai_response,
        reference=reference,
        evaluation_task=evaluation_task
    )

    response = generate_response(prompt)

    try:

        response = response.strip()

        if response.startswith("```"):
            response = re.sub(r"^```(?:json)?", "", response)
            response = response.replace("```", "").strip()

        match = re.search(r"\{.*\}", response, re.DOTALL)

        if match:
            response = match.group()

        result = json.loads(response)

    except Exception:

        result = {
            "score": None,
            "reason": "Unable to parse Groq response.",
            "evidence": response,
            "status": "ERROR"
        }

    return result


# ============================================================
# Testing
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Hallucination Detection Agent")
    print("=" * 60)

    while True:

        question = input("\nQuestion: ")

        ai_response = input("\nAI Response: ")

        reference = input("\nRetrieved Context / Reference: ")

        result = evaluate_hallucination(
            question,
            ai_response,
            reference
        )

        print("\n" + "=" * 60)
        print("Hallucination Evaluation Result")
        print("=" * 60)

        print(json.dumps(result, indent=4))

        choice = input("\nEvaluate another response? (Y/N): ").strip().lower()

        if choice != "y":
            print("\nExiting Hallucination Agent...")
            break