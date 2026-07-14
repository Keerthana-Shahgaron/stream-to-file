from fastapi import FastAPI, Request, HTTPException
from PyPDF2 import PdfReader
import io

app = FastAPI()


@app.post("/extract-pdf-text")
async def extract_pdf_text(request: Request):

    print("========== REQUEST RECEIVED ==========")

    # Print headers
    print("Headers:")
    print(dict(request.headers))

    # Read the raw PDF bytes
    pdf_bytes = await request.body()

    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Empty request body")

    try:
        # Convert bytes into a file-like object
        pdf_file = io.BytesIO(pdf_bytes)

        # Read the PDF
        reader = PdfReader(pdf_file)

        extracted_text = ""

        # Extract text from each page
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                extracted_text += f"\n----- Page {page_num} -----\n"
                extracted_text += page_text

        return {
            "success": True,
            "pageCount": len(reader.pages),
            "text": extracted_text.strip()
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process PDF: {str(e)}"
        )