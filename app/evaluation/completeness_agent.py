import json
import re

from app.evaluation.groq_eval import generate_response
from app.evaluation.prompt_templates import build_prompt


# ============================================================
# Completeness Evaluation Agent
# ============================================================

def evaluate_completeness(question, ai_response, reference):

    evaluation_task = """
Evaluate ONLY the completeness of the AI response.

Determine whether the response covers all important information needed to answer the question.

Scoring Rubric

10 = Completely answers the question.

8-9 = Covers almost everything with very small omissions.

6-7 = Covers most important points but misses some details.

4-5 = Partially answers the question.

2-3 = Covers very little.

1 = Almost incomplete.

0 = Does not answer the question.

Rules

• Evaluate ONLY completeness.
• Ignore factual accuracy.
• Ignore hallucinations.
• Ignore grammar.
• Ignore writing style.
• Ignore relevance.

• Use ONLY the supplied Reference Answer.
• Do NOT use outside knowledge.
• Do NOT invent missing points.
• Mention omissions ONLY if they appear in the reference.

If AI Response == Reference Answer,
score MUST be 10.

Return ONLY valid JSON.

{
    "score":0,
    "reason":"...",
    "evidence":"...",
    "status":"PASS"
}
"""

    prompt = build_prompt(
        question=question,
        ai_response=ai_response,
        reference=reference,
        evaluation_task=evaluation_task
    )

    response = generate_response(prompt)

    print("\n========== RAW GROQ RESPONSE ==========")
    print(response)
    print("=======================================\n")

    try:

        response = response.strip()

        # Remove markdown if present
        if response.startswith("```"):
            response = re.sub(r"^```(?:json)?", "", response)
            response = response.replace("```", "").strip()

        # Extract JSON
        match = re.search(r"\{.*\}", response, re.DOTALL)

        if match:
            response = match.group()

        # --------------------------------------------------
        # Fix invalid JSON if model returns malformed output
        # --------------------------------------------------

        response = re.sub(
            r'"reason"\s*:\s*([^"][^,]*),\s*"evidence"',
            lambda m: '"reason": "' + m.group(1).strip().replace('"', '\\"') + '", "evidence"',
            response,
            flags=re.DOTALL,
        )

        response = re.sub(
            r'"evidence"\s*:\s*([^"][^,]*),\s*"status"',
            lambda m: '"evidence": "' + m.group(1).strip().replace('"', '\\"') + '", "status"',
            response,
            flags=re.DOTALL,
        )

        response = re.sub(
            r'"status"\s*:\s*([A-Za-z]+)',
            r'"status":"\1"',
            response,
        )

        result = json.loads(response)

    except Exception as e:

        result = {
            "score": None,
            "reason": f"Unable to parse Groq response. ({e})",
            "evidence": response,
            "status": "ERROR"
        }

    return result


# ============================================================
# Testing
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Completeness Judge Agent")
    print("=" * 60)

    while True:

        question = input("\nQuestion: ")

        ai_response = input("\nAI Response: ")

        print("\nReference Answer")
        print("Paste multiple lines.")
        print("Type END on a new line when finished.\n")

        lines = []

        while True:

            line = input()

            if line.strip().upper() == "END":
                break

            lines.append(line)

        reference = "\n".join(lines)

        result = evaluate_completeness(
            question,
            ai_response,
            reference
        )

        print("\n" + "=" * 60)
        print("Completeness Evaluation Result")
        print("=" * 60)

        print(json.dumps(result, indent=4))

        choice = input("\nEvaluate another response? (Y/N): ").strip().lower()

        if choice != "y":
            print("\nExiting Completeness Agent...")
            break