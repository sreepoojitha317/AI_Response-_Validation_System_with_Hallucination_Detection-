## Development of AI Response Validation System with Hallucination Detection Assistance

**Infosys Springboard Virtual Internship 7.0**

---

## Project Overview

The **AI Response Quality Evaluator Agent** is an AI-powered system developed as part of the **Infosys Springboard Virtual Internship 7.0** to evaluate AI-generated responses across four quality dimensions:

* Accuracy
* Relevance
* Hallucination
* Completeness

The system uses a **RAG-based reference knowledge pipeline** and **multi-agent evaluation architecture** to generate dimension-wise scores, an overall score, and a final quality verdict.

It supports **single evaluation, batch evaluation, dashboard analytics, voice input, and PDF report generation**.

---

## Objectives

* Automatically evaluate AI-generated responses.
* Measure accuracy, relevance, completeness, and hallucination.
* Use reference knowledge for grounded evaluation.
* Generate overall scores and quality verdicts.
* Support batch evaluation of multiple responses.
* Provide dashboard-based analytics and PDF reports.
* Validate evaluation consistency through testing.

---

## System Architecture

```text
User
 ↓
Web UI
 ↓
FastAPI Backend
 ↓
RAG / Reference Knowledge
 ↓
┌──────────┬───────────┬──────────────┬──────────────┐
│ Accuracy │ Relevance │ Hallucination│ Completeness │
│  Agent   │   Agent   │    Agent     │    Agent     │
└──────────┴───────────┴──────────────┴──────────────┘
                    ↓
              Verdict Agent
                    ↓
          Score + Final Verdict
                    ↓
        Results / Dashboard / PDF
```

**Groq** is used for LLM-based evaluation and voice transcription.

---

## Technology Stack

| Category        | Technologies                            |
| --------------- | --------------------------------------- |
| Backend         | Python, FastAPI, Uvicorn, Jinja2        |
| Frontend        | HTML, CSS, JavaScript                   |
| LLM             | Groq API                                |
| RAG             | TruthfulQA, SQuAD, Embeddings, ChromaDB |
| Evaluation      | 4 Judge Agents + Verdict Agent          |
| Data Processing | Pandas, CSV, JSON                       |
| Reporting       | Dashboard, PDF                          |

---

## Project Structure

```text
AI_answer_Evaluation_system/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── api/
│   ├── rag/
│   ├── evaluation/
│   ├── batch/
│   ├── dashboard/
│   ├── report/
│   ├── templates/
│   └── static/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── batch_results.csv
├── requirements.txt
└── run.py
```

---

# Milestones

## Milestone 1 – Foundation

* TruthfulQA and SQuAD dataset preparation
* Preprocessing and chunking
* Embeddings and ChromaDB integration
* Reference-data retrieval
* FastAPI backend
* Web interface
* Text, PDF and Voice input

## Milestone 2 – Evaluation Agents

* Relevance Judge Agent
* Accuracy Judge Agent
* Hallucination Detection Agent
* Agent scoring and reasoning validation

## Milestone 3 – Evaluation Pipeline

* Completeness Judge Agent
* Verdict Agent
* Per-dimension results display
* Batch CSV evaluation
* Weighted overall scoring

### Scoring Weights

```text
Accuracy       30%
Relevance      25%
Hallucination  25%
Completeness   20%
```

Final verdict:

```text
PASS
NEEDS IMPROVEMENT
FAIL
```

## Milestone 4 – Analytics and Reporting

* Evaluation scoring dashboard
* Batch result analytics
* PDF report generation
* End-to-end testing
* Scoring consistency validation
* Technical documentation and project report

---

# RAG Workflow

```text
TruthfulQA + SQuAD
        ↓
Preprocessing
        ↓
Chunking
        ↓
Embeddings
        ↓
ChromaDB
        ↓
Retriever
        ↓
Relevant Reference Context
        ↓
Evaluation Agents
```

The retrieved knowledge provides supporting context for response evaluation.

---

# Evaluation Workflow

```text
Question + AI Response
          ↓
     FastAPI Backend
          ↓
    Reference / RAG
          ↓
   4 Evaluation Agents
          ↓
     Verdict Agent
          ↓
 Overall Score + Verdict
```

---

# Batch Evaluation

Users can upload a CSV containing multiple question-answer pairs.

The system automatically:

1. Validates the CSV.
2. Evaluates each response.
3. Generates dimension-wise scores.
4. Produces final verdicts.
5. Stores batch results.
6. Updates dashboard analytics.

---

# Dashboard & Reporting

The dashboard provides:

* Total evaluations
* PASS / NEEDS IMPROVEMENT / FAIL counts
* Average dimension scores
* Hallucination frequency
* Evaluation statistics

The system also generates a downloadable **PDF evaluation report** containing batch summaries, individual results, scores, findings, and verdicts.

---

# Voice Evaluation

```text
Voice Input
    ↓
Audio Upload
    ↓
Groq Transcription
    ↓
Text Response
    ↓
Evaluation Pipeline
```

---

# API Endpoints

| Method | Endpoint                  | Purpose              |
| ------ | ------------------------- | -------------------- |
| GET    | `/`                       | Home page            |
| GET    | `/results`                | Results page         |
| GET    | `/dashboard`              | Dashboard            |
| GET    | `/dashboard-data`         | Dashboard data       |
| POST   | `/evaluate`               | Single evaluation    |
| POST   | `/batch-evaluate`         | Batch evaluation     |
| POST   | `/transcribe`             | Voice transcription  |
| GET    | `/download-batch-results` | Download CSV results |
| GET    | `/dashboard/pdf`          | PDF preview          |
| GET    | `/download-dashboard-pdf` | Download PDF         |

---

# Testing

The system was tested for:

* Single evaluation
* Batch evaluation
* RAG retrieval
* Agent scoring
* Verdict generation
* Dashboard updates
* PDF generation
* Invalid inputs
* Error handling
* Scoring consistency

Repeated evaluations were also compared across accuracy, relevance, completeness, hallucination findings, and final verdicts.

---

# Installation

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI_answer_Evaluation_system

python -m venv env
env\Scripts\activate

pip install -r requirements.txt
```

Create `.env`:

```text
GROQ_API_KEY=your_groq_api_key
```

Run:

```bash
python run.py
```

or:

```bash
uvicorn app.main:app --reload
```

---

# Limitations

* Evaluation depends on the quality of reference knowledge.
* LLM-based evaluation may vary slightly between runs.
* RAG retrieval quality affects grounded evaluation.
* The system depends on the Groq API.
* Current implementation is primarily a functional evaluation prototype.

---

# Future Enhancements

* Additional LLM providers
* More benchmark datasets
* Improved claim-level hallucination detection
* Persistent evaluation history
* Advanced dashboard filters
* Additional report formats

---

# Project Outcome

The project provides a complete platform for evaluating AI-generated responses using **RAG, multi-agent judging, automated scoring, batch processing, dashboard analytics, and PDF reporting**.

```text
User
 ↓
FastAPI
 ↓
RAG / Reference Knowledge
 ↓
4 Judge Agents
 ↓
Verdict Agent
 ↓
Results
 ↓
Dashboard / PDF
```

---

## Internship Information

**Program:** Infosys Springboard Virtual Internship 7.0

**Project:** Development of AI Response Validation System with Hallucination Detection Assistance

**Domain:** Artificial Intelligence 

**Author:** Sree Poojitha Sahithi
