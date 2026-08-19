import uuid

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

import tempfile
from app.evaluation.groq_transcription import transcribe_audio

from app.evaluation.accuracy_agent import evaluate_accuracy
from app.evaluation.relevance_agent import evaluate_relevance
from app.evaluation.hallucination_agent import evaluate_hallucination
from app.evaluation.completeness_agent import evaluate_completeness
from app.evaluation.verdict_agent import evaluate_verdict
from app.report.dashboard_pdf import generate_dashboard_pdf

from app.dashboard.dashboard_utils import load_dashboard_data

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


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

    print("RESULTS PAGE LOADED")

    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "version": "batch-test"
        }
    )
# ==========================================================
# DASHBOARD PAGE
# ==========================================================

@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="dashboard.html"

    )

# ==========================================================
# DASHBOARD DATA API
# ==========================================================

@router.get("/dashboard-data")
def dashboard_data():

    dashboard = load_dashboard_data()

    if dashboard is None:

        raise HTTPException(

            status_code=404,

            detail="No batch evaluation data found."

        )

    return dashboard

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

        print("\n" + "=" * 70)
        print("❌ SINGLE EVALUATION ERROR")
        print("=" * 70)

        print("Error type:", type(e).__name__)
        print("Error:", str(e))

        import traceback
        traceback.print_exc()

        print("=" * 70)

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

        print("\n" + "=" * 70)
        print("BATCH EVALUATION STARTED")
        print("=" * 70)

        # ----------------------------------------------------
        # Validate CSV
        # ----------------------------------------------------

        if not file.filename.endswith(".csv"):

            raise HTTPException(
                status_code=400,
                detail="Please upload a CSV file."
            )

        print("Uploaded file:", file.filename)

        # ----------------------------------------------------
        # Save Uploaded CSV
        # ----------------------------------------------------

        upload_dir = "uploads"

        os.makedirs(
            upload_dir,
            exist_ok=True
        )

        uploaded_csv = os.path.join(
            upload_dir,
            file.filename
        )

        with open(
            uploaded_csv,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        print(
            "CSV saved:",
            uploaded_csv
        )

        # ----------------------------------------------------
        # Remove previous dashboard results
        # ----------------------------------------------------

        if os.path.exists(
            "batch_results.csv"
        ):

            os.remove(
                "batch_results.csv"
            )

            print(
                "Old batch_results.csv removed"
            )

        # ----------------------------------------------------
        # Run Batch Evaluation
        # ----------------------------------------------------

        print(
            "Starting evaluate_csv()..."
        )

        batch_result = evaluate_csv(
            uploaded_csv
        )

        print(
            "evaluate_csv() completed"
        )

        print(
            "Batch result:",
            batch_result
        )

        # ----------------------------------------------------
        # Validate batch result
        # ----------------------------------------------------

        if batch_result is None:

            raise Exception(
                "evaluate_csv() returned None"
            )

        if "summary" not in batch_result:

            raise Exception(
                "Batch result does not contain 'summary'"
            )

        if "results" not in batch_result:

            raise Exception(
                "Batch result does not contain 'results'"
            )

        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        print(
            "BATCH EVALUATION COMPLETED SUCCESSFULLY"
        )

        return {

            "success": True,

            "filename": file.filename,

            "summary":
                batch_result["summary"],

            "results":
                batch_result["results"]

        }

    except HTTPException:

        raise

    except Exception as e:

        print("\n" + "=" * 70)
        print("❌ BATCH EVALUATION ERROR")
        print("=" * 70)

        print(
            "Error type:",
            type(e).__name__
        )

        print(
            "Error:",
            str(e)
        )

        import traceback

        traceback.print_exc()

        print("=" * 70)

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
# ==========================================================
# VOICE TRANSCRIPTION API
# ==========================================================

@router.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):

    try:

        suffix = os.path.splitext(audio.filename)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            shutil.copyfileobj(
                audio.file,
                temp_file
            )

            temp_path = temp_file.name

        transcript = transcribe_audio(temp_path)

        os.remove(temp_path)

        return {
            "transcript": transcript
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
# ==========================================================
# pdf generation manual 
# ==========================================================

@router.get("/dashboard/pdf", response_class=HTMLResponse)
async def dashboard_pdf(request: Request):

    dashboard = load_dashboard_data()

    if dashboard is None:
        raise HTTPException(
            status_code=404,
            detail="No dashboard data available"
        )

    return templates.TemplateResponse(
        request=request,
        name="dashboard_pdf.html",
        context={
            "dashboard": dashboard
        }
    )
# ==========================================================
# Dashboard download
# ==========================================================
# ==========================================================
# Dashboard download
# ==========================================================

@router.get("/download-dashboard-pdf")
def download_dashboard_pdf(request: Request):
    import uuid

    output_file = f"Evaluation_Dashboard_{uuid.uuid4().hex}.pdf"

    base_url = str(request.base_url).rstrip("/")

    generate_dashboard_pdf(
        f"{base_url}/dashboard/pdf",
        output_file
    )

    return FileResponse(
        path=output_file,
        media_type="application/pdf",
        filename="Evaluation_Dashboard.pdf"
    )