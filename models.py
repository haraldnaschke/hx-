from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class EngineType(str, Enum):
    v6 = "V6"
    v8 = "V8"
    v12 = "V12"
    hybrid = "Hybrid"


class Ferrari(BaseModel):
    id: Optional[int] = None
    model: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1947, le=2030)
    engine: EngineType
    horsepower: int = Field(..., gt=0)
    top_speed_kmh: int = Field(..., gt=0)
    price_usd: float = Field(..., gt=0)

    model_config = {"json_schema_extra": {"example": {
        "model": "SF90 Stradale",
        "year": 2023,
        "engine": "Hybrid",
        "horsepower": 986,
        "top_speed_kmh": 340,
        "price_usd": 507000,
    }}}


class FerrariUpdate(BaseModel):
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1947, le=2030)
    engine: Optional[EngineType] = None
    horsepower: Optional[int] = Field(None, gt=0)
    top_speed_kmh: Optional[int] = Field(None, gt=0)
    price_usd: Optional[float] = Field(None, gt=0)
