import os
import subprocess
import sys
from pathlib import Path


# ============================================================
# Deployment RAG Builder
# ============================================================
# Purpose:
#   Build the complete RAG pipeline on Render in the correct
#   order without modifying the existing RAG scripts.
#
# Order:
#   1. load_data.py
#   2. preprocess.py
#   3. chunking.py
#   4. vector_store.py
#
# This script is intended to run during Render BUILD.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parent


# ============================================================
# Required Input Files
# ============================================================

REQUIRED_FILES = [
    PROJECT_ROOT / "data" / "raw" / "TruthfulQA.csv",
    PROJECT_ROOT / "data" / "raw" / "train-v1.1.json",
    PROJECT_ROOT / "data" / "raw" / "dev-v1.1.json",
]


# ============================================================
# RAG Pipeline
# ============================================================

RAG_SCRIPTS = [
    PROJECT_ROOT / "app" / "rag" / "load_data.py",
    PROJECT_ROOT / "app" / "rag" / "preprocess.py",
    PROJECT_ROOT / "app" / "rag" / "chunking.py",
    PROJECT_ROOT / "app" / "rag" / "vector_store.py",
]


def run_script(script_path: Path) -> None:
    """Run one RAG pipeline script and stop if it fails."""

    print("\n" + "=" * 70)
    print(f"RUNNING: {script_path}")
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=False,
    )

    if result.returncode != 0:
        print("\n" + "=" * 70)
        print(f"FAILED: {script_path}")
        print(f"Exit Code: {result.returncode}")
        print("=" * 70)

        raise SystemExit(result.returncode)

    print("\n" + "=" * 70)
    print(f"COMPLETED: {script_path}")
    print("=" * 70)


def validate_inputs() -> None:
    """Verify that all datasets required by the RAG pipeline exist."""

    print("\nChecking required dataset files...")

    missing_files = [
        str(path)
        for path in REQUIRED_FILES
        if not path.exists()
    ]

    if missing_files:
        print("\nMissing required files:")

        for file_path in missing_files:
            print(f"  - {file_path}")

        raise SystemExit(
            "RAG build stopped because required dataset files are missing."
        )

    print("All required dataset files are available.")


def validate_scripts() -> None:
    """Verify that all RAG scripts exist."""

    print("\nChecking RAG pipeline scripts...")

    missing_scripts = [
        str(path)
        for path in RAG_SCRIPTS
        if not path.exists()
    ]

    if missing_scripts:
        print("\nMissing RAG scripts:")

        for script_path in missing_scripts:
            print(f"  - {script_path}")

        raise SystemExit(
            "RAG build stopped because required scripts are missing."
        )

    print("All RAG pipeline scripts are available.")


def validate_outputs() -> None:
    """Verify that the RAG database was created successfully."""

    processed_dataset = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "processed_dataset.csv"
    )

    chunks_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "chunks.pkl"
    )

    chroma_db = (
        PROJECT_ROOT
        / "data"
        / "chroma_db"
    )

    print("\n" + "=" * 70)
    print("VALIDATING RAG BUILD")
    print("=" * 70)

    if not processed_dataset.exists():
        raise SystemExit(
            "RAG build failed: processed_dataset.csv was not created."
        )

    if not chunks_file.exists():
        raise SystemExit(
            "RAG build failed: chunks.pkl was not created."
        )

    if not chroma_db.exists():
        raise SystemExit(
            "RAG build failed: ChromaDB directory was not created."
        )

    chroma_files = list(chroma_db.rglob("*"))

    if not any(path.is_file() for path in chroma_files):
        raise SystemExit(
            "RAG build failed: ChromaDB directory is empty."
        )

    print("Processed dataset      : OK")
    print("Chunks file            : OK")
    print("ChromaDB               : OK")
    print("RAG build validation   : SUCCESS")


def main() -> None:

    print("\n" + "=" * 70)
    print("AI RESPONSE QUALITY EVALUATOR")
    print("RENDER RAG BUILD")
    print("=" * 70)

    print(f"\nProject Root: {PROJECT_ROOT}")

    # --------------------------------------------------------
    # Validate source files
    # --------------------------------------------------------

    validate_inputs()
    validate_scripts()

    # --------------------------------------------------------
    # Execute RAG pipeline
    # --------------------------------------------------------

    for script in RAG_SCRIPTS:
        run_script(script)

    # --------------------------------------------------------
    # Validate generated RAG artifacts
    # --------------------------------------------------------

    validate_outputs()

    # --------------------------------------------------------
    # Finished
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("RAG BUILD COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nRender can now start the FastAPI application.")


if __name__ == "__main__":
    main()