from pydantic import BaseModel


class HealthStatus(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"
