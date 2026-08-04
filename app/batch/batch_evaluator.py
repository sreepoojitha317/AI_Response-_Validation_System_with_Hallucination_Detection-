import pandas as pd

from app.evaluation.accuracy_agent import evaluate_accuracy
from app.evaluation.relevance_agent import evaluate_relevance
from app.evaluation.hallucination_agent import evaluate_hallucination
from app.evaluation.completeness_agent import evaluate_completeness
from app.evaluation.verdict_agent import evaluate_verdict


# ============================================================
# Batch Evaluation
# ============================================================

def evaluate_csv(csv_path):
    """
    Evaluates every Question-Answer pair inside a CSV file.

    Required columns:
        question
        answer
        context
    """

    df = pd.read_csv(csv_path)

    results = []

    print("=" * 70)
    print("BATCH EVALUATION STARTED")
    print("=" * 70)

    for index, row in df.iterrows():

        question = str(row["question"])
        ai_response = str(row["answer"])
        reference = str(row["context"])

        print(f"\nEvaluating Row {index + 1}...")

        # Accuracy
        accuracy = evaluate_accuracy(
            question,
            ai_response,
            reference
        )

        # Relevance
        relevance = evaluate_relevance(
            question,
            ai_response,
            reference
        )

        # Hallucination
        hallucination = evaluate_hallucination(
            question,
            ai_response,
            reference
        )

        # Completeness
        completeness = evaluate_completeness(
            question,
            ai_response,
            reference
        )

        # Verdict
        verdict = evaluate_verdict(
            accuracy,
            relevance,
            hallucination,
            completeness
        )

        result = {

            "question": question,

            "ai_response": ai_response,

            "reference": reference,

            "accuracy_score": accuracy["score"],

            "relevance_score": relevance["score"],

            "hallucination_score": hallucination["score"],

            "completeness_score": completeness["score"],

            "overall_score": verdict["overall_score"],

            "verdict": verdict["verdict"],

            "summary": verdict["summary"]

        }

        results.append(result)

        print(
            f"Completed Row {index + 1} | "
            f"Overall Score: {verdict['overall_score']}% | "
            f"Verdict: {verdict['verdict']}"
        )

    # ============================================================
    # Save CSV
    # ============================================================

    results_df = pd.DataFrame(results)

    output_file = "batch_results.csv"

    results_df.to_csv(
        output_file,
        index=False
    )

    # ============================================================
    # Batch Summary
    # ============================================================

    total_questions = len(results)

    average_score = round(
        results_df["overall_score"].mean(),
        2
    )

    pass_count = len(
        results_df[
            results_df["verdict"] == "PASS"
        ]
    )

    needs_improvement_count = len(
        results_df[
            results_df["verdict"] == "NEEDS IMPROVEMENT"
        ]
    )

    fail_count = len(
        results_df[
            results_df["verdict"] == "FAIL"
        ]
    )

    summary = {

        "total_questions": total_questions,

        "average_score": average_score,

        "pass_count": pass_count,

        "needs_improvement_count": needs_improvement_count,

        "fail_count": fail_count,

        "output_file": output_file

    }

    print("\n" + "=" * 70)
    print("BATCH EVALUATION COMPLETED")
    print("=" * 70)

    print(f"Results saved to: {output_file}")

    return {

        "summary": summary,

        "results": results

    }


# ============================================================
# Testing
# ============================================================

if __name__ == "__main__":

    csv_path = "data/processed/merged_dataset.csv"

    batch_result = evaluate_csv(csv_path)

    print("\nBatch Summary\n")

    print(batch_result["summary"])