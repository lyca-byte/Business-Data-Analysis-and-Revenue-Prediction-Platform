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


# ---------------------------------------------------------
# Serverless Hugging Face Cache Configuration
# ---------------------------------------------------------

CACHE_DIR = "/tmp/huggingface"

os.environ["HF_HOME"] = CACHE_DIR
os.environ["HF_HUB_CACHE"] = os.path.join(CACHE_DIR, "hub")

os.makedirs(CACHE_DIR, exist_ok=True)


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
        self.load_error = None


    # -----------------------------------------------------
    # Load Model
    # -----------------------------------------------------

    def load(self):

        # Prevent repeated loading
        if self.is_loaded:

            print("[model] Model already loaded.")

            return


        try:

            print("=" * 60)
            print("[model] Starting model loading process")

            print(
                f"[model] HF_REPO_ID: {HF_REPO_ID}"
            )

            print(
                f"[model] HF_TOKEN available: "
                f"{bool(HF_TOKEN)}"
            )

            print(
                f"[model] Cache directory: "
                f"{CACHE_DIR}"
            )

            print("=" * 60)


            # -------------------------------------------------
            # Download Model
            # -------------------------------------------------

            print(
                "[model] Downloading "
                "revenue_prediction_model.pkl"
            )

            model_path = hf_hub_download(

                repo_id=HF_REPO_ID,

                filename="revenue_prediction_model.pkl",

                token=HF_TOKEN if HF_TOKEN else None,

                cache_dir=CACHE_DIR,

                force_download=False,

            )


            # -------------------------------------------------
            # Download Preprocessing
            # -------------------------------------------------

            print(
                "[model] Downloading preprocessing.pkl"
            )

            scaler_path = hf_hub_download(

                repo_id=HF_REPO_ID,

                filename="preprocessing.pkl",

                token=HF_TOKEN if HF_TOKEN else None,

                cache_dir=CACHE_DIR,

                force_download=False,

            )


            # -------------------------------------------------
            # Download Metadata
            # -------------------------------------------------

            print(
                "[model] Downloading model_metadata.json"
            )

            metadata_path = hf_hub_download(

                repo_id=HF_REPO_ID,

                filename="model_metadata.json",

                token=HF_TOKEN if HF_TOKEN else None,

                cache_dir=CACHE_DIR,

                force_download=False,

            )


            # -------------------------------------------------
            # Load Joblib Artifacts
            # -------------------------------------------------

            print(
                "[model] Loading joblib artifacts"
            )


            self.model = joblib.load(

                model_path

            )


            self.scaler = joblib.load(

                scaler_path

            )


            # -------------------------------------------------
            # Load Metadata
            # -------------------------------------------------

            print(
                "[model] Loading metadata"
            )


            with open(

                metadata_path,

                "r",

                encoding="utf-8"

            ) as file:

                self.metadata = json.load(

                    file

                )


            self.is_loaded = True

            self.load_error = None


            print("=" * 60)

            print(
                "[model] Model loaded successfully"
            )

            print(
                f"[model] Model name: "
                f"{self.metadata.get('model_name')}"
            )

            print(
                f"[model] Features: "
                f"{self.metadata.get('features')}"
            )

            print("=" * 60)


        except Exception as e:

            self.is_loaded = False

            self.load_error = str(e)


            print("=" * 60)

            print(
                "[model] MODEL LOADING FAILED"
            )

            print(
                f"[model] Error type: "
                f"{type(e).__name__}"
            )

            print(
                f"[model] Error message: "
                f"{str(e)}"
            )

            print(
                "[model] Full traceback:"
            )

            traceback.print_exc()

            print("=" * 60)


            # IMPORTANT:
            # Do not crash the entire Vercel function.
            return False


        return True


    # -----------------------------------------------------
    # Ensure Model Loaded
    # -----------------------------------------------------

    def ensure_loaded(self):

        if self.is_loaded:

            return True


        print(
            "[model] Model not loaded."
        )

        print(
            "[model] Attempting to load model..."
        )


        return self.load()


    # -----------------------------------------------------
    # Properties
    # -----------------------------------------------------

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


# ---------------------------------------------------------
# Global Model Loader
# ---------------------------------------------------------

model_loader = ModelLoader()