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
import os
import traceback

import joblib
from huggingface_hub import hf_hub_download

from backend.config.settings import HF_REPO_ID, HF_TOKEN


CACHE_DIR = "/tmp/huggingface"

os.environ["HF_HOME"] = CACHE_DIR
os.environ["HF_HUB_CACHE"] = os.path.join(CACHE_DIR, "hub")

os.makedirs(CACHE_DIR, exist_ok=True)


class ModelLoader:

    def __init__(self):
        self.model = None
        self.scaler = None
        self.metadata = None

        self.is_loaded = False
        self.load_error = None

    def load(self):

        if self.is_loaded:
            return True

        try:
            print("=" * 60)
            print("[MODEL] Starting model loading")
            print(f"[MODEL] HF_REPO_ID = {HF_REPO_ID}")
            print(f"[MODEL] HF_TOKEN configured = {bool(HF_TOKEN)}")
            print(f"[MODEL] Cache = {CACHE_DIR}")
            print("=" * 60)

            if not HF_REPO_ID:
                raise RuntimeError(
                    "HF_REPO_ID environment variable is empty."
                )

            # -------------------------------------------------
            # Model
            # -------------------------------------------------

            print(
                "[MODEL] Downloading revenue_prediction_model.pkl"
            )

            model_path = hf_hub_download(
                repo_id=HF_REPO_ID,
                filename="revenue_prediction_model.pkl",
                token=HF_TOKEN or None,
                cache_dir=CACHE_DIR,
            )

            print(f"[MODEL] Model path: {model_path}")

            # -------------------------------------------------
            # Preprocessing
            # -------------------------------------------------

            print(
                "[MODEL] Downloading preprocessing.pkl"
            )

            preprocessing_path = hf_hub_download(
                repo_id=HF_REPO_ID,
                filename="preprocessing.pkl",
                token=HF_TOKEN or None,
                cache_dir=CACHE_DIR,
            )

            print(
                f"[MODEL] Preprocessing path: "
                f"{preprocessing_path}"
            )

            # -------------------------------------------------
            # Metadata
            # -------------------------------------------------

            print(
                "[MODEL] Downloading model_metadata.json"
            )

            metadata_path = hf_hub_download(
                repo_id=HF_REPO_ID,
                filename="model_metadata.json",
                token=HF_TOKEN or None,
                cache_dir=CACHE_DIR,
            )

            print(
                f"[MODEL] Metadata path: "
                f"{metadata_path}"
            )

            # -------------------------------------------------
            # Load files
            # -------------------------------------------------

            print("[MODEL] Loading model")

            self.model = joblib.load(model_path)

            print("[MODEL] Loading preprocessing")

            self.scaler = joblib.load(preprocessing_path)

            print("[MODEL] Loading metadata")

            with open(
                metadata_path,
                "r",
                encoding="utf-8",
            ) as f:
                self.metadata = json.load(f)

            self.is_loaded = True
            self.load_error = None

            print("=" * 60)
            print("[MODEL] MODEL LOADED SUCCESSFULLY")
            print("=" * 60)

            return True

        except Exception as e:

            self.is_loaded = False
            self.load_error = (
                f"{type(e).__name__}: {str(e)}"
            )

            print("=" * 60)
            print("[MODEL] MODEL LOADING FAILED")
            print(
                f"[MODEL] {self.load_error}"
            )
            print("=" * 60)

            traceback.print_exc()

            return False

    def ensure_loaded(self):
        if self.is_loaded:
            return True

        return self.load()


    @property
    def feature_columns(self):

        if not self.is_loaded:
            raise RuntimeError(
                "Model is not loaded."
            )

        return self.metadata["features"]


    @property
    def model_name(self):

        if not self.is_loaded:
            raise RuntimeError(
                "Model is not loaded."
            )

        return self.metadata["model_name"]


    @property
    def model_type(self):

        if not self.is_loaded:
            raise RuntimeError(
                "Model is not loaded."
            )

        return self.metadata["model_type"]


model_loader = ModelLoader()