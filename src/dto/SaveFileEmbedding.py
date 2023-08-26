from pydantic import BaseModel


class SaveFileEmbedding(BaseModel):
    fileName: str
