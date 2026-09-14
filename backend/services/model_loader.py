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

from huggingface_hub import hf_hub_download

from backend.config.settings import (
    HF_REPO_ID,
    HF_TOKEN,
)

class ModelLoader:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.metadata = None
        self.is_loaded = False

    def load(self):

        print("Starting model loading process...")
        print(f"Hugging Face Repository: {HF_REPO_ID}")

        print("Downloading revenue prediction model...")

        model_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename="revenue_prediction_model.pkl",
            token=HF_TOKEN,
        )

        print("Downloading preprocessing artifact...")

        scaler_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename="preprocessing.pkl",
            token=HF_TOKEN,
        )

        print("Downloading metadata...")

        metadata_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename="model_metadata.json",
            token=HF_TOKEN,
        )

        print("Loading model artifacts...")

        self.model = joblib.load(model_path)

        self.scaler = joblib.load(scaler_path)

        with open(metadata_path, "r") as file:
            self.metadata = json.load(file)

        self.is_loaded = True

        print("Model loaded successfully.")


    @property
    def feature_columns(self):
        if not self.is_loaded:
            raise RuntimeError(
                "ModelLoader has not been loaded."
            )
        return self.metadata["features"]


    @property
    def model_name(self):
        if not self.is_loaded:
            raise RuntimeError(
                "ModelLoader has not been loaded."
            )
        return self.metadata["model_name"]


    @property
    def model_type(self):
        if not self.is_loaded:
            raise RuntimeError(
                "ModelLoader has not been loaded."
            )
        return self.metadata["model_type"]

model_loader = ModelLoader()