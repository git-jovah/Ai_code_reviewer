from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ReviewRequest, ReviewResponse
from app.services.gemini import GeminiService

app = FastAPI(title="Code Reviewer API")

# Enable CORS so the Streamlit frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_service = GeminiService()

@app.get("/health")
def health():
    return {"status": "online"}

@app.post("/review_code", response_model=ReviewResponse)
async def review_code(request: ReviewRequest):
    try:
        return await gemini_service.get_code_review(request.code, request.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))