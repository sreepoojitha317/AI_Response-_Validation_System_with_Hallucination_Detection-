import json


# ============================================================
# Verdict Agent
# ============================================================

def evaluate_verdict(
    accuracy,
    relevance,
    hallucination,
    completeness
):
    """
    Aggregates all judge scores and produces
    an overall evaluation verdict.
    """

    # ============================================================
    # Weighted Scoring Model
    # ============================================================

    accuracy_weight = 0.30
    relevance_weight = 0.25
    hallucination_weight = 0.25
    completeness_weight = 0.20

    # Weighted score out of 10
    weighted_score = (

        accuracy["score"] * accuracy_weight +

        relevance["score"] * relevance_weight +

        hallucination["score"] * hallucination_weight +

        completeness["score"] * completeness_weight

    )

    # Convert to percentage
    overall_score = round(weighted_score * 10, 2)

    # ============================================================
    # Verdict
    # ============================================================

    if overall_score >= 90:

        verdict = "PASS"

    elif overall_score >= 70:

        verdict = "NEEDS IMPROVEMENT"

    else:

        verdict = "FAIL"

    # ============================================================
    # Consolidated Summary
    # ============================================================

    reasons = []

    reasons.append(
        f"Accuracy: {accuracy['reason']}"
    )

    reasons.append(
        f"Relevance: {relevance['reason']}"
    )

    reasons.append(
        f"Hallucination: {hallucination['reason']}"
    )

    reasons.append(
        f"Completeness: {completeness['reason']}"
    )

    return {

        "overall_score": overall_score,

        "verdict": verdict,

        "summary": " | ".join(reasons)

    }


# ============================================================
# Testing
# ============================================================

if __name__ == "__main__":

    accuracy = {

        "score": 10,
        "reason": "Matches reference."

    }

    relevance = {

        "score": 10,
        "reason": "Directly answers question."

    }

    hallucination = {

        "score": 10,
        "reason": "No unsupported claims."

    }

    completeness = {

        "score": 9,
        "reason": "Minor information missing."

    }

    result = evaluate_verdict(

        accuracy,

        relevance,

        hallucination,

        completeness

    )

    print("=" * 60)
    print("Verdict Agent")
    print("=" * 60)

    print(f"Overall Score : {result['overall_score']}%")
    print(f"Verdict       : {result['verdict']}")
    print(f"Summary       : {result['summary']}")

    print("\nJSON Output:\n")
    print(json.dumps(result, indent=4))