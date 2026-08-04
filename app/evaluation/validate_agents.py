import pandas as pd

from app.evaluation.accuracy_agent import evaluate_accuracy
from app.evaluation.relevance_agent import evaluate_relevance
from app.evaluation.hallucination_agent import evaluate_hallucination
from app.evaluation.completeness_agent import evaluate_completeness
from app.evaluation.verdict_agent import evaluate_verdict


# ============================================================
# Load Benchmark Dataset
# ============================================================

DATASET_PATH = "data/processed/merged_dataset.csv"

df = pd.read_csv(DATASET_PATH)

# Validate only first 2 samples
df = df.head(2)

print("=" * 70)
print("VALIDATING JUDGE AGENTS ON BENCHMARK DATASET")
print("=" * 70)

for i, row in df.iterrows():

    question = str(row["question"])
    reference = str(row["answer"])
    context = str(row["context"])
    source = str(row["source"])

    # ============================================================
    # Use Benchmark Answer as AI Response
    # ============================================================

    ai_response = reference

    print("\n" + "=" * 70)
    print(f"Sample {i + 1}")
    print("=" * 70)

    print("\nQuestion:")
    print(question)

    print("\nAI Response:")
    print(ai_response)

    print("\nReference Answer:")
    print(reference)

    # ============================================================
    # Accuracy Agent
    # ============================================================

    accuracy = evaluate_accuracy(
        question,
        ai_response,
        reference
    )

    # ============================================================
    # Relevance Agent
    # ============================================================

    relevance = evaluate_relevance(
        question,
        ai_response,
        reference
    )

    # ============================================================
    # Hallucination Agent
    # ============================================================

    hallucination = evaluate_hallucination(
        question,
        ai_response,
        reference
    )

    # ============================================================
    # Completeness Agent
    # ============================================================

    completeness = evaluate_completeness(
        question,
        ai_response,
        reference
    )

    # ============================================================
    # Verdict Agent
    # ============================================================

    verdict = evaluate_verdict(
        accuracy,
        relevance,
        hallucination,
        completeness
    )

    # ============================================================
    # Individual Scores
    # ============================================================

    print("\n---------------- AGENT SCORES ----------------")

    print(f"Accuracy Score      : {accuracy['score']}/10")
    print(f"Relevance Score     : {relevance['score']}/10")
    print(f"Hallucination Score : {hallucination['score']}/10")
    print(f"Completeness Score  : {completeness['score']}/10")

    # ============================================================
    # Reasons
    # ============================================================

    print("\n---------------- REASONS ----------------")

    print(f"Accuracy      : {accuracy['reason']}")
    print(f"Relevance     : {relevance['reason']}")
    print(f"Hallucination : {hallucination['reason']}")
    print(f"Completeness  : {completeness['reason']}")

    # ============================================================
    # Overall Verdict
    # ============================================================

    print("\n---------------- OVERALL VERDICT ----------------")

    print(f"Overall Score : {verdict['overall_score']}%")
    print(f"Verdict       : {verdict['verdict']}")

    print("\nSummary:")
    print(verdict["summary"])

    # ============================================================
    # Supporting Evidence
    # ============================================================

    print("\n---------------- SUPPORTING EVIDENCE ----------------")

    print("\nReference Answer:")
    print(reference)

    print("\nReference Context:")
    print(context)

    print("\nDataset Source:")
    print(source)

print("\n" + "=" * 70)
print("BENCHMARK VALIDATION COMPLETED SUCCESSFULLY")
print("=" * 70)