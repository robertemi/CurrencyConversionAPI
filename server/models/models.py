from pydantic import BaseModel, Field

class ConversionRequest(BaseModel):
    user_query: str