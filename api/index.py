import os

# Vercel filesystem is read-only except /tmp.
# Hugging Face cache must therefore use /tmp.
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["HF_HUB_CACHE"] = "/tmp/huggingface/hub"
os.environ["XDG_CACHE_HOME"] = "/tmp"

from backend.main import app