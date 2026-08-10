import os
import pandas as pd


# ==========================================================
# LOAD DASHBOARD DATA
# ==========================================================

def load_dashboard_data():
    """
    Reads batch_results.csv and computes:

    1. KPI statistics
    2. Batch summary
    3. Dimension-wise average scores
    4. Individual evaluation results
    5. Improvement recommendations
    """

    file_path = "batch_results.csv"

    # ------------------------------------------------------
    # Check File Exists
    # ------------------------------------------------------

    if not os.path.exists(file_path):
        return None

    # ------------------------------------------------------
    # Read CSV
    # ------------------------------------------------------

    try:

        df = pd.read_csv(file_path)

    except Exception as e:

        print(
            "Error reading batch_results.csv:",
            e
        )

        return None

    if df.empty:
        return None

    # ------------------------------------------------------
    # Required Columns
    # ------------------------------------------------------

    required_columns = [

        "question",
        "accuracy_score",
        "relevance_score",
        "hallucination_score",
        "completeness_score",
        "overall_score",
        "verdict"

    ]

    missing_columns = [

        column
        for column in required_columns
        if column not in df.columns

    ]

    if missing_columns:

        print(
            "Missing columns in batch_results.csv:",
            missing_columns
        )

        return None

    # ------------------------------------------------------
    # Convert Scores To Numeric
    # ------------------------------------------------------

    score_columns = [

        "accuracy_score",
        "relevance_score",
        "hallucination_score",
        "completeness_score",
        "overall_score"

    ]

    for column in score_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # ------------------------------------------------------
    # Remove Invalid Rows
    # ------------------------------------------------------

    df = df.dropna(
        subset=score_columns
    )

    if df.empty:
        return None

    # ======================================================
    # OVERALL COUNTS
    # ======================================================

    total = len(df)

    verdict_series = (
        df["verdict"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    pass_count = len(
        df[
            verdict_series == "PASS"
        ]
    )

    needs_count = len(
        df[
            verdict_series.isin([
                "NEEDS IMPROVEMENT",
                "NEEDS_IMPROVEMENT"
            ])
        ]
    )

    fail_count = len(
        df[
            verdict_series == "FAIL"
        ]
    )

    # ======================================================
    # AVERAGE SCORES
    # ======================================================

    average_accuracy = round(
        float(
            df["accuracy_score"].mean()
        ),
        2
    )

    average_relevance = round(
        float(
            df["relevance_score"].mean()
        ),
        2
    )

    average_hallucination = round(
        float(
            df["hallucination_score"].mean()
        ),
        2
    )

    average_completeness = round(
        float(
            df["completeness_score"].mean()
        ),
        2
    )

    average_overall = round(
        float(
            df["overall_score"].mean()
        ),
        2
    )

    # ======================================================
    # HALLUCINATION FREQUENCY
    #
    # Score below 8 = possible hallucination
    # ======================================================

    hallucination_frequency = len(
        df[
            df["hallucination_score"] < 8
        ]
    )

    # ======================================================
    # INDIVIDUAL EVALUATION RESULTS
    # ======================================================

    individual_results = []

    for _, row in df.iterrows():

        individual_results.append({

            "question": str(
                row["question"]
            ),

            "accuracy": round(
                float(
                    row["accuracy_score"]
                ),
                2
            ),

            "relevance": round(
                float(
                    row["relevance_score"]
                ),
                2
            ),

            "hallucination": round(
                float(
                    row["hallucination_score"]
                ),
                2
            ),

            "completeness": round(
                float(
                    row["completeness_score"]
                ),
                2
            ),

            "overall": round(
                float(
                    row["overall_score"]
                ),
                2
            ),

            "verdict": str(
                row["verdict"]
            )

        })

    # ======================================================
    # IMPROVEMENT RECOMMENDATIONS
    # ======================================================

    recommendations = []

    # ------------------------------------------------------
    # Accuracy Recommendation
    # ------------------------------------------------------

    if average_accuracy < 8:

        recommendations.append({

            "dimension": "Accuracy",

            "icon": "🎯",

            "severity": "High",

            "message":
                "Improve factual correctness by "
                "verifying important claims against "
                "reliable reference information."

        })

    elif average_accuracy < 9:

        recommendations.append({

            "dimension": "Accuracy",

            "icon": "🎯",

            "severity": "Medium",

            "message":
                "Accuracy is reasonable, but factual "
                "claims should be checked more carefully "
                "against the reference context."

        })

    # ------------------------------------------------------
    # Relevance Recommendation
    # ------------------------------------------------------

    if average_relevance < 8:

        recommendations.append({

            "dimension": "Relevance",

            "icon": "🔗",

            "severity": "High",

            "message":
                "Responses should focus more directly "
                "on the user's question and avoid "
                "unnecessary information."

        })

    elif average_relevance < 9:

        recommendations.append({

            "dimension": "Relevance",

            "icon": "🔗",

            "severity": "Medium",

            "message":
                "Improve relevance by keeping answers "
                "focused and directly aligned with "
                "the question."

        })

    # ------------------------------------------------------
    # Hallucination Recommendation
    # ------------------------------------------------------

    if average_hallucination < 8:

        recommendations.append({

            "dimension": "Hallucination",

            "icon": "🧠",

            "severity": "High",

            "message":
                "Reduce unsupported claims by grounding "
                "responses in the provided reference "
                "context and retrieved knowledge."

        })

    elif average_hallucination < 9:

        recommendations.append({

            "dimension": "Hallucination",

            "icon": "🧠",

            "severity": "Medium",

            "message":
                "Some responses may contain unsupported "
                "claims. Strengthen grounding and "
                "reference verification."

        })

    # ------------------------------------------------------
    # Completeness Recommendation
    # ------------------------------------------------------

    if average_completeness < 8:

        recommendations.append({

            "dimension": "Completeness",

            "icon": "📄",

            "severity": "High",

            "message":
                "Responses should address all important "
                "parts of the question and include "
                "necessary supporting information."

        })

    elif average_completeness < 9:

        recommendations.append({

            "dimension": "Completeness",

            "icon": "📄",

            "severity": "Medium",

            "message":
                "Improve completeness by covering all "
                "key requirements of the question."

        })

    # ------------------------------------------------------
    # Overall Recommendation
    # ------------------------------------------------------

    if average_overall < 70:

        recommendations.append({

            "dimension": "Overall Quality",

            "icon": "⭐",

            "severity": "High",

            "message":
                "Overall response quality is low. "
                "Focus on improving accuracy, relevance, "
                "hallucination control, and completeness."

        })

    elif average_overall < 90:

        recommendations.append({

            "dimension": "Overall Quality",

            "icon": "⭐",

            "severity": "Medium",

            "message":
                "Overall quality can be improved by "
                "strengthening the weaker evaluation "
                "dimensions."

        })

    else:

        recommendations.append({

            "dimension": "Overall Quality",

            "icon": "⭐",

            "severity": "Good",

            "message":
                "Overall response quality is strong. "
                "Continue maintaining factual accuracy, "
                "relevance, grounding, and completeness."

        })

    # ======================================================
    # RETURN DASHBOARD DATA
    # ======================================================

    return {

        # --------------------------------------------------
        # KPI DATA
        # --------------------------------------------------

        "total": total,

        "pass_count": pass_count,

        "needs_count": needs_count,

        "fail_count": fail_count,

        "average_accuracy": average_accuracy,

        "average_relevance": average_relevance,

        "average_hallucination":
            average_hallucination,

        "average_completeness":
            average_completeness,

        "average_overall":
            average_overall,

        "hallucination_frequency":
            hallucination_frequency,

        # --------------------------------------------------
        # BATCH SUMMARY
        # --------------------------------------------------

        "batch_summary": {

            "total_evaluations": total,

            "average_score":
                average_overall,

            "pass":
                pass_count,

            "needs_improvement":
                needs_count,

            "fail":
                fail_count

        },

        # --------------------------------------------------
        # DIMENSION SCORES
        # --------------------------------------------------

        "dimension_scores": {

            "accuracy":
                average_accuracy,

            "relevance":
                average_relevance,

            "hallucination":
                average_hallucination,

            "completeness":
                average_completeness

        },

        # --------------------------------------------------
        # INDIVIDUAL RESULTS
        # --------------------------------------------------

        "individual_results":
            individual_results,

        # --------------------------------------------------
        # RECOMMENDATIONS
        # --------------------------------------------------

        "recommendations":
            recommendations

    }


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    dashboard = load_dashboard_data()

    print("=" * 70)

    print("DASHBOARD DATA")

    print("=" * 70)

    print(dashboard)