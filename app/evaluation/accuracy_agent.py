import json

from app.evaluation.groq_eval import generate_response
from app.evaluation.prompt_templates import build_prompt


# ============================================================
# Accuracy Evaluation Agent
# ============================================================

def evaluate_accuracy(question, ai_response, reference):
    """
    Evaluates the factual accuracy of an AI response.
    """

    evaluation_task = """
Evaluate ONLY the factual accuracy of the AI response.

Compare the AI response with the reference answer or retrieved context.

Scoring Rubric:

10 = Completely accurate. Every fact matches the reference.

8-9 = Mostly accurate. Contains only very minor factual mistakes or wording issues.

6-7 = Generally accurate but misses one or two important facts OR contains one moderate factual mistake.

4-5 = Partially accurate. Some information is correct but several facts are incorrect or missing.

2-3 = Mostly inaccurate. Only a small part of the response is factually correct.

1 = Almost completely incorrect.

0 = Completely incorrect or directly contradicts the reference.

Evaluation Rules:

- Evaluate ONLY factual accuracy.
- Ignore grammar and writing style.
- Ignore completeness.
- Ignore relevance.
- Penalize factual mistakes according to their severity.
- Use intermediate scores (2-9) whenever appropriate.
- Give 10 ONLY if every important fact is correct.
- Give 0 ONLY if the response is completely wrong or contradicts the reference.

IMPORTANT:

Return ONLY a valid JSON object.

Do NOT write explanations outside JSON.
Do NOT use markdown.
Do NOT use ```json.

Return exactly these fields:

{
    "score": 0,
    "reason": "",
    "evidence": "",
    "status": ""
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
    print("Accuracy Judge Agent")
    print("=" * 60)

    while True:

        question = input("\nQuestion: ")

        ai_response = input("\nAI Response: ")

        reference = input("\nReference Answer: ")

        result = evaluate_accuracy(
            question,
            ai_response,
            reference
        )

        print("\n" + "=" * 60)
        print("Accuracy Evaluation Result")
        print("=" * 60)

        print(json.dumps(result, indent=4))

        choice = input(
            "\nEvaluate another response? (Y/N): "
        ).strip().lower()

        if choice != "y":

            print("\nExiting Accuracy Agent...")
            break