from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    UploadFile,
    File
)

from fastapi.responses import (
    HTMLResponse,
    FileResponse
)

import os
import shutil

from fastapi.templating import Jinja2Templates

from app.batch.batch_evaluator import evaluate_csv
from app.schemas import EvaluationRequest

from app.evaluation.accuracy_agent import evaluate_accuracy
from app.evaluation.relevance_agent import evaluate_relevance
from app.evaluation.hallucination_agent import evaluate_hallucination
from app.evaluation.completeness_agent import evaluate_completeness
from app.evaluation.verdict_agent import evaluate_verdict

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# ==========================================================
# HOME PAGE
# ==========================================================

@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ==========================================================
# RESULTS PAGE
# ==========================================================

@router.get("/results", response_class=HTMLResponse)
def results(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="results.html"
    )


# ==========================================================
# SINGLE EVALUATION API
# ==========================================================

@router.post("/evaluate")
def evaluate(data: EvaluationRequest):

    try:

        question = data.question
        ai_response = data.ai_response
        reference = data.reference

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

        return {

            "accuracy": accuracy,

            "relevance": relevance,

            "hallucination": hallucination,

            "completeness": completeness,

            "verdict": verdict

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# BATCH EVALUATION API
# ==========================================================

@router.post("/batch-evaluate")
async def batch_evaluate(
    file: UploadFile = File(...)
):

    try:

        # ----------------------------------------------------
        # Validate CSV
        # ----------------------------------------------------

        if not file.filename.endswith(".csv"):

            raise HTTPException(
                status_code=400,
                detail="Please upload a CSV file."
            )

        # ----------------------------------------------------
        # Save Uploaded CSV
        # ----------------------------------------------------

        upload_dir = "uploads"

        os.makedirs(upload_dir, exist_ok=True)

        uploaded_csv = os.path.join(
            upload_dir,
            file.filename
        )

        with open(uploaded_csv, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # ----------------------------------------------------
        # Run Batch Evaluation
        # ----------------------------------------------------

        batch_result = evaluate_csv(uploaded_csv)
        
        # -----------------------------------------
        # Return JSON to Frontend
        # ----------------------------------------------------

        return {

    "success": True,

    "filename": file.filename,

    "summary": batch_result["summary"],

    "results": batch_result["results"]

   }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# DOWNLOAD BATCH RESULTS
# ==========================================================

@router.get("/download-batch-results")
def download_batch_results():

    output_file = "batch_results.csv"

    if not os.path.exists(output_file):

        raise HTTPException(
            status_code=404,
            detail="Batch results not found."
        )

    return FileResponse(

        path=output_file,

        media_type="text/csv",

        filename="batch_results.csv"

    )