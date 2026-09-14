import os

# Vercel Serverless Functions have a read-only filesystem except for /tmp.
# huggingface_hub defaults its cache to $HOME/.cache/huggingface, which is
# NOT writable on Vercel and crashes the function on startup. Redirect the
# cache to /tmp BEFORE huggingface_hub (imported later via backend.main ->
# model_loader) is loaded, since its cache path is resolved at import time.
os.environ.setdefault("HF_HOME", "/tmp/huggingface")
os.environ.setdefault("HF_HUB_CACHE", "/tmp/huggingface/hub")

from backend.main import app