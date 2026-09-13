"""
model_loader.py
---------------
Loads and holds the trained model artifacts in memory.

Design decision — load at startup, not per-request:
    Loading a .pkl file involves disk I/O and object deserialization.
    On every prediction request, this would add unnecessary latency.
    By loading once at application startup and keeping the objects in
    memory, every prediction request is served immediately.

    For a model this size (<2KB), memory cost is negligible.

Usage:
    from backend.services.model_loader import model_loader
    model_loader.load()          # called once at startup
    model_loader.model           # the LinearRegression object
    model_loader.scaler          # the StandardScaler object
    model_loader.metadata        # the dict from model_metadata.json
"""

import json
import joblib

from backend.config.settings import MODEL_PATH, SCALER_PATH, METADATA_PATH


class ModelLoader:
    """
    Singleton-style container for the trained model artifacts.

    Attributes:
        model    -- fitted sklearn LinearRegression instance
        scaler   -- fitted sklearn StandardScaler instance
        metadata -- dict loaded from model_metadata.json
        is_loaded -- bool, True after load() succeeds
    """

    def __init__(self):
        self.model     = None
        self.scaler    = None
        self.metadata  = None
        self.is_loaded = False

    def load(self) -> None:
        """
        Load all three model artifacts from disk.
        Raises FileNotFoundError if any artifact is missing.
        Call this once at application startup via FastAPI lifespan.
        """
        # Load the trained LinearRegression model
        self.model = joblib.load(MODEL_PATH)

        # Load the fitted StandardScaler
        self.scaler = joblib.load(SCALER_PATH)

        # Load the metadata JSON
        with open(METADATA_PATH, "r") as f:
            self.metadata = json.load(f)

        self.is_loaded = True

    @property
    def feature_columns(self) -> list[str]:
        """Return the ordered list of feature names from metadata."""
        if not self.is_loaded:
            raise RuntimeError("ModelLoader has not been loaded yet.")
        return self.metadata["features"]

    @property
    def model_name(self) -> str:
        if not self.is_loaded:
            raise RuntimeError("ModelLoader has not been loaded yet.")
        return self.metadata["model_name"]

    @property
    def model_type(self) -> str:
        if not self.is_loaded:
            raise RuntimeError("ModelLoader has not been loaded yet.")
        return self.metadata["model_type"]


# Single shared instance — imported by predictor.py and main.py
model_loader = ModelLoader()
