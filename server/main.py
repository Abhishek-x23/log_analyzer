from fastapi import FastAPI, UploadFile, File, HTTPException
from analyzer.parser import analyze_logs

app = FastAPI(
    title="Log Analyzer API",
    description="REST API for analyzing application logs",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze_log_file(file: UploadFile = File(...)):

    # Check file extension
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are supported"
        )

    try:
        # Read uploaded file
        content = await file.read()

        # Decode file content
        text = content.decode("utf-8")

        # Convert content into individual lines
        lines = text.splitlines()

        # Analyze the logs
        result = analyze_logs(lines)

        return result

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must contain valid UTF-8 text"
        )

    finally:
        await file.close()