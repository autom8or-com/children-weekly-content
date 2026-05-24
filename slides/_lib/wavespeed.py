"""
WaveSpeed AI API client for Nano Banana image generation.
Supports text-to-image, edit, edit-fast, and edit-ultra modes.

API base: https://api.wavespeed.ai/api/v3
Submit:   POST /google/{model}/{mode}
Poll:     GET  /predictions/{task-id}
"""
import base64
import os
import time
import requests
from pathlib import Path


API_BASE = "https://api.wavespeed.ai/api/v3"

ENDPOINTS = {
    "nano-banana-pro": {
        "text-to-image": "google/nano-banana-pro/text-to-image",
        "edit":          "google/nano-banana-pro/edit",
        "edit-ultra":    "google/nano-banana-pro/edit-ultra",
    },
    "nano-banana-2": {
        "edit":          "google/nano-banana-2/edit",
        "edit-fast":     "google/nano-banana-2/edit-fast",
    },
}

COST_PER_IMAGE = {
    ("nano-banana-pro", "text-to-image", "1k"): 0.14,
    ("nano-banana-pro", "text-to-image", "2k"): 0.14,
    ("nano-banana-pro", "text-to-image", "4k"): 0.24,
    ("nano-banana-pro", "edit",          "1k"): 0.14,
    ("nano-banana-pro", "edit",          "2k"): 0.14,
    ("nano-banana-pro", "edit",          "4k"): 0.14,
    ("nano-banana-pro", "edit-ultra",    "4k"): 0.15,
    ("nano-banana-pro", "edit-ultra",    "8k"): 0.15,
    ("nano-banana-2",   "edit",          "1k"): 0.07,
    ("nano-banana-2",   "edit",          "2k"): 0.105,
    ("nano-banana-2",   "edit",          "4k"): 0.14,
    ("nano-banana-2",   "edit-fast",     "2k"): 0.045,
    ("nano-banana-2",   "edit-fast",     "4k"): 0.045,
}


class WaveSpeedClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ["WAVESPEEDAI_API_KEY"]
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        self.total_cost = 0.0

    def generate(
        self,
        prompt: str,
        mode: str = "text-to-image",
        model: str = "nano-banana-pro",
        images: list[str] | None = None,
        aspect_ratio: str = "16:9",
        resolution: str = "2k",
        output_format: str = "png",
        poll_interval: int = 5,
        max_wait: int = 300,
    ) -> str:
        """Submit a generation request and poll until complete. Returns output image URL."""
        endpoint = ENDPOINTS[model][mode]
        url = f"{API_BASE}/{endpoint}"

        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "output_format": output_format,
        }
        if images:
            payload["images"] = [self._encode_image(img) for img in images]

        for attempt in range(1, 4):
            try:
                resp = self.session.post(url, json=payload, timeout=120)
                break
            except Exception as exc:
                if attempt == 3:
                    raise
                print(f"  → POST attempt {attempt} failed ({exc.__class__.__name__}) — retrying")
                time.sleep(3 * attempt)
        resp.raise_for_status()
        body = resp.json()
        task_id = body["data"]["id"]
        print(f"  → submitted task {task_id}")

        # Poll for completion
        poll_url = f"{API_BASE}/predictions/{task_id}/result"
        elapsed = 0
        while elapsed < max_wait:
            time.sleep(poll_interval)
            elapsed += poll_interval
            for poll_attempt in range(1, 4):
                try:
                    r = self.session.get(poll_url, timeout=30)
                    break
                except Exception as exc:
                    if poll_attempt == 3:
                        raise
                    print(f"  → poll attempt {poll_attempt} failed ({exc.__class__.__name__}) — retrying")
                    time.sleep(3 * poll_attempt)
            r.raise_for_status()
            data = r.json()["data"]
            status = data["status"]
            print(f"  → [{elapsed}s] status: {status}")
            if status == "completed":
                cost = COST_PER_IMAGE.get((model, mode, resolution), 0)
                self.total_cost += cost
                return data["outputs"][0]
            if status == "failed":
                raise RuntimeError(f"Generation failed: {data}")

        raise TimeoutError(f"Generation timed out after {max_wait}s — task {task_id}")

    def _encode_image(self, img: str) -> str:
        """Convert a local file path to a base64 data URI; pass through URLs unchanged."""
        p = Path(img)
        if p.exists():
            data = base64.b64encode(p.read_bytes()).decode()
            suffix = p.suffix.lstrip(".").lower()
            mime = "image/png" if suffix == "png" else "image/jpeg"
            return f"data:{mime};base64,{data}"
        return img  # already a URL

    def download(self, image_url: str, save_path: str | Path) -> Path:
        """Download generated image to disk."""
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        resp = requests.get(image_url)
        resp.raise_for_status()
        save_path.write_bytes(resp.content)
        return save_path
