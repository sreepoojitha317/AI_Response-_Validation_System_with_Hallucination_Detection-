from pydantic import BaseModel


class EvaluationRequest(BaseModel):

    question: str

    ai_response: str

    reference: str