import google.generativeai as genai
import json
from app.core.config import settings
from app.schemas import ReviewResponse

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)

    async def get_code_review(self, code: str, language: str) -> ReviewResponse:
        prompt = f"""
        Act as an expert senior developer. Review this {language} code.
        Provide a structured JSON response with:
        - security_issues (list)
        - performance_issues (list)
        - readability_issues (list)
        - overall_score (0-100)
        
        Code:
        {code}
        """
        try:
            # Constrain Gemini to return valid JSON
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            return ReviewResponse(**data)
        except Exception as e:
            raise ValueError(f"AI Provider Error: {str(e)}")