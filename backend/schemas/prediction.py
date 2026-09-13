"""
prediction.py
-------------
Pydantic models for the /predict endpoint.

PredictionRequest  — validates incoming user input
PredictionResponse — defines the structure of the prediction result
"""

from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    """
    Input schema for POST /predict.

    Each field maps directly to one of the 7 model input features.
    Field constraints mirror the synthetic dataset ranges and prevent
    the model from receiving values it was never trained on.

    Pydantic automatically returns HTTP 422 with a clear error message
    if any field is missing or fails validation.
    """

    marketing_spend: float = Field(
        ...,
        ge=0,
        description="Amount spent on marketing activities (USD). Must be >= 0.",
        examples=[10000.0],
    )
    advertising_spend: float = Field(
        ...,
        ge=0,
        description="Amount spent on advertising campaigns (USD). Must be >= 0.",
        examples=[5000.0],
    )
    website_traffic: float = Field(
        ...,
        ge=0,
        description="Number of monthly website visitors. Must be >= 0.",
        examples=[50000.0],
    )
    number_of_customers: float = Field(
        ...,
        ge=0,
        description="Number of customers in the period. Must be >= 0.",
        examples=[1200.0],
    )
    product_price: float = Field(
        ...,
        gt=0,
        description="Average product price (USD). Must be > 0.",
        examples=[50.0],
    )
    discount_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Discount percentage offered (0–100).",
        examples=[10.0],
    )
    previous_revenue: float = Field(
        ...,
        ge=0,
        description="Revenue from the previous period (USD). Must be >= 0.",
        examples=[100000.0],
    )

    @field_validator("marketing_spend", "advertising_spend", "website_traffic",
                     "number_of_customers", "previous_revenue")
    @classmethod
    def must_not_be_negative(cls, v: float) -> float:
        """Extra guard: reject negative values (redundant with ge=0 but explicit)."""
        if v < 0:
            raise ValueError("Value must be non-negative.")
        return v

    @field_validator("product_price")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Product price must be greater than zero.")
        return v

    @field_validator("discount_percentage")
    @classmethod
    def discount_in_range(cls, v: float) -> float:
        if not (0 <= v <= 100):
            raise ValueError("Discount percentage must be between 0 and 100.")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "marketing_spend": 10000.0,
                "advertising_spend": 5000.0,
                "website_traffic": 50000.0,
                "number_of_customers": 1200.0,
                "product_price": 50.0,
                "discount_percentage": 10.0,
                "previous_revenue": 100000.0,
            }
        }
    }


class PredictionResponse(BaseModel):
    """
    Output schema for POST /predict.

    Returns the predicted revenue along with context information
    so the frontend knows how to display the result.
    """

    model_config = {"protected_namespaces": ()}

    predicted_revenue: float = Field(
        ...,
        description="Predicted revenue in USD.",
    )
    currency: str = Field(
        default="USD",
        description="Currency of the predicted revenue.",
    )
    model: str = Field(
        ...,
        description="Name of the model that generated the prediction.",
    )
    model_type: str = Field(
        ...,
        description="Type/algorithm of the model.",
    )


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
