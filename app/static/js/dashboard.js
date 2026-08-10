// ==========================================================
// AI RESPONSE EVALUATION DASHBOARD
// ==========================================================


// ==========================================================
// GLOBAL CHART REFERENCES
// ==========================================================

let pieChartInstance = null;
let barChartInstance = null;
let radarChartInstance = null;


// ==========================================================
// FETCH DASHBOARD DATA
// ==========================================================

async function loadDashboard() {

    try {

        const response =
            await fetch("/dashboard-data");


        if (!response.ok) {

            throw new Error(
                `Dashboard API failed: ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "Dashboard Data:",
            data
        );


        // ==================================================
        // KPI STATISTICS
        // ==================================================

        animateValue(
            "total",
            data.total || 0
        );


        animateValue(
            "pass",
            data.pass_count || 0
        );


        animateValue(
            "needs",
            data.needs_count || 0
        );


        animateValue(
            "fail",
            data.fail_count || 0
        );


        animateValue(
            "accuracy",
            data.average_accuracy || 0
        );


        animateValue(
            "relevance",
            data.average_relevance || 0
        );


        animateValue(
            "completeness",
            data.average_completeness || 0
        );


        animateValue(
            "hallucination",
            data.average_hallucination || 0
        );


        animateValue(
            "frequency",
            data.hallucination_frequency || 0
        );


        animateValue(
            "overall",
            data.average_overall || 0,
            "%"
        );


        // ==================================================
        // BATCH SUMMARY
        // ==================================================

        updateBatchSummary(data);


        // ==================================================
        // DIMENSION-WISE SCORES
        // ==================================================

        updateDimensionScores(data);


        // ==================================================
        // INDIVIDUAL EVALUATION RESULTS
        // ==================================================

        updateIndividualResults(data);


        // ==================================================
        // IMPROVEMENT RECOMMENDATIONS
        // ==================================================

        updateRecommendations(data);


        // ==================================================
        // CHARTS
        // ==================================================

        createPieChart(data);

        createBarChart(data);

        createRadarChart(data);


    }

    catch (error) {

        console.error(
            "Dashboard loading error:",
            error
        );

    }

}


// ==========================================================
// ANIMATED COUNTER
// ==========================================================

function animateValue(
    id,
    value,
    suffix = ""
) {

    const element =
        document.getElementById(id);


    if (!element) {

        return;

    }


    value =
        Number(value) || 0;


    let start = 0;


    const duration = 1000;


    const step =
        value / (duration / 20);


    // ------------------------------------------------------
    // Prevent multiple intervals
    // ------------------------------------------------------

    if (element.dataset.timer) {

        clearInterval(
            Number(element.dataset.timer)
        );

    }


    const timer =
        setInterval(() => {

            start += step;


            if (start >= value) {

                element.innerHTML =
                    Number.isInteger(value)
                        ? value + suffix
                        : value.toFixed(1) + suffix;


                clearInterval(timer);


                delete element.dataset.timer;

            }

            else {

                element.innerHTML =
                    start.toFixed(1) + suffix;

            }

        }, 20);


    element.dataset.timer = timer;

}


// ==========================================================
// BATCH SUMMARY
// ==========================================================

function updateBatchSummary(data) {

    const summary =
        data.batch_summary || {};


    // ------------------------------------------------------
    // Total Evaluations
    // ------------------------------------------------------

    const totalElement =
        document.getElementById(
            "summary-total"
        );


    if (totalElement) {

        totalElement.textContent =
            summary.total_evaluations ??
            data.total ??
            0;

    }


    // ------------------------------------------------------
    // Average Score
    // ------------------------------------------------------

    const averageElement =
        document.getElementById(
            "summary-average"
        );


    if (averageElement) {

        const average =
            summary.average_score ??
            data.average_overall ??
            0;


        averageElement.textContent =
            Number(average).toFixed(1) + "%";

    }


    // ------------------------------------------------------
    // PASS
    // ------------------------------------------------------

    const passElement =
        document.getElementById(
            "summary-pass"
        );


    if (passElement) {

        passElement.textContent =
            summary.pass ??
            data.pass_count ??
            0;

    }


    // ------------------------------------------------------
    // NEEDS IMPROVEMENT
    // ------------------------------------------------------

    const needsElement =
        document.getElementById(
            "summary-needs"
        );


    if (needsElement) {

        needsElement.textContent =
            summary.needs_improvement ??
            data.needs_count ??
            0;

    }


    // ------------------------------------------------------
    // FAIL
    // ------------------------------------------------------

    const failElement =
        document.getElementById(
            "summary-fail"
        );


    if (failElement) {

        failElement.textContent =
            summary.fail ??
            data.fail_count ??
            0;

    }

}


// ==========================================================
// DIMENSION-WISE SCORES
// ==========================================================

function updateDimensionScores(data) {

    const dimensions =
        data.dimension_scores || {};


    // ------------------------------------------------------
    // Accuracy
    // ------------------------------------------------------

    const accuracyElement =
        document.getElementById(
            "dimension-accuracy"
        );


    if (accuracyElement) {

        accuracyElement.textContent =
            formatScore(
                dimensions.accuracy ??
                data.average_accuracy
            );

    }


    // ------------------------------------------------------
    // Relevance
    // ------------------------------------------------------

    const relevanceElement =
        document.getElementById(
            "dimension-relevance"
        );


    if (relevanceElement) {

        relevanceElement.textContent =
            formatScore(
                dimensions.relevance ??
                data.average_relevance
            );

    }


    // ------------------------------------------------------
    // Hallucination
    // ------------------------------------------------------

    const hallucinationElement =
        document.getElementById(
            "dimension-hallucination"
        );


    if (hallucinationElement) {

        hallucinationElement.textContent =
            formatScore(
                dimensions.hallucination ??
                data.average_hallucination
            );

    }


    // ------------------------------------------------------
    // Completeness
    // ------------------------------------------------------

    const completenessElement =
        document.getElementById(
            "dimension-completeness"
        );


    if (completenessElement) {

        completenessElement.textContent =
            formatScore(
                dimensions.completeness ??
                data.average_completeness
            );

    }

}


// ==========================================================
// FORMAT SCORE
// ==========================================================

function formatScore(value) {

    value =
        Number(value) || 0;


    return value.toFixed(1) + "/10";

}


// ==========================================================
// INDIVIDUAL EVALUATION RESULTS
// ==========================================================

function updateIndividualResults(data) {

    const tableBody =
        document.getElementById(
            "evaluation-results-body"
        );


    if (!tableBody) {

        console.warn(
            "evaluation-results-body not found."
        );

        return;

    }


    // ------------------------------------------------------
    // Clear existing rows
    // ------------------------------------------------------

    tableBody.innerHTML = "";


    const results =
        data.individual_results || [];


    // ------------------------------------------------------
    // No results
    // ------------------------------------------------------

    if (results.length === 0) {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td
                colspan="7"
                class="no-results"
            >
                No evaluation results available.
            </td>

        `;


        tableBody.appendChild(row);


        return;

    }


    // ------------------------------------------------------
    // Create rows
    // ------------------------------------------------------

    results.forEach(
        (result, index) => {

            const row =
                document.createElement("tr");


            // ----------------------------------------------
            // Question
            // ----------------------------------------------

            const question =
                escapeHTML(
                    result.question || "—"
                );


            // ----------------------------------------------
            // Dimension scores
            // ----------------------------------------------

            const accuracy =
                formatScore(
                    result.accuracy
                );


            const relevance =
                formatScore(
                    result.relevance
                );


            const hallucination =
                formatScore(
                    result.hallucination
                );


            const completeness =
                formatScore(
                    result.completeness
                );


            // ----------------------------------------------
            // Overall score
            // ----------------------------------------------

            const overall =
                Number(
                    result.overall || 0
                ).toFixed(1);


            // ----------------------------------------------
            // Verdict
            // ----------------------------------------------

            const verdict =
                String(
                    result.verdict || "—"
                )
                .toUpperCase()
                .trim();


            let verdictClass =
                "verdict-default";


            if (verdict === "PASS") {

                verdictClass =
                    "verdict-pass";

            }


            else if (

                verdict ===
                    "NEEDS IMPROVEMENT"

                ||

                verdict ===
                    "NEEDS_IMPROVEMENT"

            ) {

                verdictClass =
                    "verdict-needs";

            }


            else if (
                verdict === "FAIL"
            ) {

                verdictClass =
                    "verdict-fail";

            }


            // ----------------------------------------------
            // Row HTML
            // ----------------------------------------------

            row.innerHTML = `

                <td class="question-cell">
                    ${question}
                </td>


                <td>
                    <span class="score-badge">
                        ${accuracy}
                    </span>
                </td>


                <td>
                    <span class="score-badge">
                        ${relevance}
                    </span>
                </td>


                <td>
                    <span class="score-badge">
                        ${hallucination}
                    </span>
                </td>


                <td>
                    <span class="score-badge">
                        ${completeness}
                    </span>
                </td>


                <td>
                    <strong class="overall-score">
                        ${overall}%
                    </strong>
                </td>


                <td>
                    <span
                        class="
                            verdict-badge
                            ${verdictClass}
                        "
                    >
                        ${verdict}
                    </span>
                </td>

            `;


            tableBody.appendChild(row);

        }
    );

}


// ==========================================================
// IMPROVEMENT RECOMMENDATIONS
// ==========================================================

function updateRecommendations(data) {

    const container =
        document.getElementById(
            "recommendations-container"
        );


    // ------------------------------------------------------
    // Check container
    // ------------------------------------------------------

    if (!container) {

        console.warn(
            "recommendations-container not found."
        );

        return;

    }


    // ------------------------------------------------------
    // Clear previous recommendations
    // ------------------------------------------------------

    container.innerHTML = "";


    const recommendations =
        data.recommendations || [];


    // ------------------------------------------------------
    // No recommendations
    // ------------------------------------------------------

    if (
        recommendations.length === 0
    ) {

        container.innerHTML = `

            <div class="recommendation-card good">

                <div class="recommendation-icon">
                    ⭐
                </div>

                <div class="recommendation-content">

                    <h3>
                        Good Performance
                    </h3>

                    <p>
                        No major improvement areas
                        were identified.
                    </p>

                </div>

            </div>

        `;


        return;

    }


    // ------------------------------------------------------
    // Create recommendation cards
    // ------------------------------------------------------

    recommendations.forEach(
        recommendation => {

            const card =
                document.createElement(
                    "div"
                );


            const severity =
                String(
                    recommendation.severity ||
                    "Medium"
                )
                .toLowerCase();


            card.className =
                `recommendation-card ${severity}`;


            const icon =
                escapeHTML(
                    recommendation.icon ||
                    "💡"
                );


            const dimension =
                escapeHTML(
                    recommendation.dimension ||
                    "Improvement Area"
                );


            const message =
                escapeHTML(
                    recommendation.message ||
                    ""
                );


            const severityText =
                escapeHTML(
                    recommendation.severity ||
                    "Medium"
                );


            card.innerHTML = `

                <div class="recommendation-icon">
                    ${icon}
                </div>


                <div class="recommendation-content">

                    <div class="recommendation-header">

                        <h3>
                            ${dimension}
                        </h3>


                        <span
                            class="
                                recommendation-severity
                            "
                        >
                            ${severityText}
                        </span>

                    </div>


                    <p>
                        ${message}
                    </p>

                </div>

            `;


            container.appendChild(card);

        }
    );

}


// ==========================================================
// HTML ESCAPE
// Prevent text from breaking the UI
// ==========================================================

function escapeHTML(value) {

    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}


// ==========================================================
// PIE CHART
// ==========================================================

function createPieChart(data) {

    const canvas =
        document.getElementById(
            "pieChart"
        );


    if (!canvas) {

        return;

    }


    // ------------------------------------------------------
    // Check Chart.js
    // ------------------------------------------------------

    if (
        typeof Chart === "undefined"
    ) {

        console.error(
            "Chart.js is not loaded."
        );

        return;

    }


    const ctx =
        canvas.getContext("2d");


    // ------------------------------------------------------
    // Destroy previous chart
    // ------------------------------------------------------

    if (pieChartInstance) {

        pieChartInstance.destroy();

    }


    pieChartInstance =
        new Chart(
            ctx,
            {

                type: "pie",


                data: {

                    labels: [

                        "PASS",

                        "Needs Improvement",

                        "FAIL"

                    ],


                    datasets: [{

                        data: [

                            Number(
                                data.pass_count || 0
                            ),

                            Number(
                                data.needs_count || 0
                            ),

                            Number(
                                data.fail_count || 0
                            )

                        ],


                        backgroundColor: [

                            "#22C55E",

                            "#F59E0B",

                            "#EF4444"

                        ],


                        borderWidth: 3,

                        borderColor:
                            "#FFFFFF"

                    }]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,


                    plugins: {

                        legend: {

                            position: "bottom",

                            labels: {

                                padding: 20,

                                font: {

                                    size: 13

                                }

                            }

                        }

                    },


                    animation: {

                        animateRotate: true,

                        duration: 1000

                    }

                }

            }
        );

}


// ==========================================================
// BAR CHART
// ==========================================================

function createBarChart(data) {

    const canvas =
        document.getElementById(
            "barChart"
        );


    if (!canvas) {

        return;

    }


    if (
        typeof Chart === "undefined"
    ) {

        console.error(
            "Chart.js is not loaded."
        );

        return;

    }


    const ctx =
        canvas.getContext("2d");


    // ------------------------------------------------------
    // Destroy previous chart
    // ------------------------------------------------------

    if (barChartInstance) {

        barChartInstance.destroy();

    }


    barChartInstance =
        new Chart(
            ctx,
            {

                type: "bar",


                data: {

                    labels: [

                        "Accuracy",

                        "Relevance",

                        "Completeness",

                        "Hallucination"

                    ],


                    datasets: [{

                        label:
                            "Average Score",


                        data: [

                            Number(
                                data.average_accuracy || 0
                            ),

                            Number(
                                data.average_relevance || 0
                            ),

                            Number(
                                data.average_completeness || 0
                            ),

                            Number(
                                data.average_hallucination || 0
                            )

                        ],


                        backgroundColor: [

                            "#7B4DFF",

                            "#9365FF",

                            "#AF86FF",

                            "#B99AFF"

                        ],


                        borderRadius: 10,

                        borderSkipped: false

                    }]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,


                    plugins: {

                        legend: {

                            display: false

                        }

                    },


                    scales: {

                        y: {

                            beginAtZero: true,

                            max: 10,


                            ticks: {

                                stepSize: 2

                            }

                        }

                    },


                    animation: {

                        duration: 1000

                    }

                }

            }
        );

}


// ==========================================================
// RADAR CHART
// ==========================================================

function createRadarChart(data) {

    const canvas =
        document.getElementById(
            "radarChart"
        );


    if (!canvas) {

        return;

    }


    if (
        typeof Chart === "undefined"
    ) {

        console.error(
            "Chart.js is not loaded."
        );

        return;

    }


    const ctx =
        canvas.getContext("2d");


    // ------------------------------------------------------
    // Destroy previous chart
    // ------------------------------------------------------

    if (radarChartInstance) {

        radarChartInstance.destroy();

    }


    radarChartInstance =
        new Chart(
            ctx,
            {

                type: "radar",


                data: {

                    labels: [

                        "Accuracy",

                        "Relevance",

                        "Completeness",

                        "Hallucination",

                        "Overall Score"

                    ],


                    datasets: [{

                        label:
                            "AI Evaluation Profile",


                        data: [

                            Number(
                                data.average_accuracy || 0
                            ),

                            Number(
                                data.average_relevance || 0
                            ),

                            Number(
                                data.average_completeness || 0
                            ),

                            Number(
                                data.average_hallucination || 0
                            ),

                            Number(
                                data.average_overall || 0
                            ) / 10

                        ],


                        backgroundColor:
                            "rgba(123,77,255,0.20)",


                        borderColor:
                            "#7B4DFF",


                        borderWidth: 3,


                        pointBackgroundColor:
                            "#7B4DFF",


                        pointBorderColor:
                            "#FFFFFF",


                        pointRadius: 5,


                        pointHoverRadius: 7

                    }]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,


                    plugins: {

                        legend: {

                            position: "bottom"

                        }

                    },


                    scales: {

                        r: {

                            min: 0,

                            max: 10,


                            ticks: {

                                stepSize: 2,

                                backdropColor:
                                    "transparent"

                            },


                            grid: {

                                color:
                                    "#E8DDFE"

                            },


                            angleLines: {

                                color:
                                    "#E8DDFE"

                            },


                            pointLabels: {

                                color:
                                    "#555",


                                font: {

                                    size: 13,

                                    weight: "bold"

                                }

                            }

                        }

                    }

                }

            }
        );

}


// ==========================================================
// PDF DOWNLOAD
// ==========================================================

function downloadPDF() {

    window.location.href =
        "/download-dashboard-pdf";

}


// ==========================================================
// LOAD DASHBOARD
// ==========================================================

window.addEventListener(
    "load",
    loadDashboard
);