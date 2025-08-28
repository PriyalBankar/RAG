from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from utilities.constants import DEFAULT_MODEL_NAME


class ModelName(str, Enum):
    MISTRAL_7B = DEFAULT_MODEL_NAME


class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.MISTRAL_7B)


class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName
    reasoning: str = Field(default="", description="Model's reasoning process")
    sources: list[str] = Field(default=[], description="Source documents used")
    confidence: float = Field(default=0.0, description="Model's confidence in the answer")


class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime


class DeleteFileRequest(BaseModel):
    file_id: int
