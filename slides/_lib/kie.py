"""
kie.ai API client for Nano Banana image generation.

Mirrors the WaveSpeedClient interface (generate / download / total_cost) so the
pipeline can swap providers without other code changes. See slides/_lib/provider.py.

Unlike WaveSpeed (inline base64), kie.ai's job API takes reference images as public
URLs only. Local files are therefore uploaded first via the base64-upload endpoint,
which returns a temporary URL (auto-deleted after ~3 days — fine for a generation run).

Flow:
  (edit only) POST  https://kieai.redpandaai.co/api/file-base64-upload  → downloadUrl
              POST  https://api.kie.ai/api/v1/jobs/createTask           → taskId
  poll        GET   https://api.kie.ai/api/v1/jobs/recordInfo?taskId=   → state/resultJson
"""
import base64
import json
import os
import time
import requests
from pathlib import Path


API_BASE      = "https://api.kie.ai/api/v1"
UPLOAD_URL    = "https://kieai.redpandaai.co/api/file-base64-upload"
CREATE_URL    = f"{API_BASE}/jobs/createTask"
RECORD_URL    = f"{API_BASE}/jobs/recordInfo"
CREDIT_URL    = f"{API_BASE}/chat/credit"

# kie.ai job models accept the same names scenes.json already uses. For both, the
# unified createTask endpoint infers edit-vs-generate from whether image_input is
# populated — there is no separate edit model string (that only applies to the legacy
# google/nano-banana family, which this pipeline does not use).
SUPPORTED_MODELS = {"nano-banana-pro", "nano-banana-2"}

# Max reference images the API accepts per model (extras would be rejected).
MAX_IMAGES = {"nano-banana-pro": 8, "nano-banana-2": 14}

# Dollar estimate per image (kie.ai bills in credits; exact credits are summed from
# the API in total_credits — these are only for the human-readable "$ so far" line).
COST_PER_IMAGE = {
    ("nano-banana-pro", "1k"): 0.10,
    ("nano-banana-pro", "2k"): 0.12,
    ("nano-banana-pro", "4k"): 0.20,
    ("nano-banana-2",   "1k"): 0.04,
    ("nano-banana-2",   "2k"): 0.06,
    ("nano-banana-2",   "4k"): 0.08,
}


class KieClient:
    name = "kie"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ["KIE_API_KEY"]
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        self.total_cost = 0.0      # dollar estimate
        self.total_credits = 0     # exact, from API

    # -- public interface (matches WaveSpeedClient) --------------------------

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
        max_wait: int = 600,
    ) -> str:
        """Submit a generation request and poll until complete. Returns output image URL.

        `mode` is accepted for interface parity but kie.ai's job API infers edit vs
        text-to-image from whether image_input is populated — there is no separate edit
        endpoint, so the mode string itself is not sent.
        """
        if model not in SUPPORTED_MODELS:
            raise ValueError(f"kie.ai: unsupported model {model!r} (expected one of {SUPPORTED_MODELS})")

        cap = MAX_IMAGES.get(model, 8)
        if images and len(images) > cap:
            print(f"  [WARN] {len(images)} refs exceed {model} limit of {cap} — using first {cap}")
            images = images[:cap]
        image_input = [self._to_url(img) for img in images] if images else []

        payload = {
            "model": model,
            "input": {
                "prompt": prompt,
                "image_input": image_input,
                "aspect_ratio": aspect_ratio,
                "resolution": resolution.upper(),     # "2k" -> "2K"
                "output_format": output_format,
            },
        }

        body = self._post(CREATE_URL, payload, label="createTask")
        task_id = body["data"]["taskId"]
        print(f"  → submitted task {task_id}")

        elapsed = 0
        while elapsed < max_wait:
            time.sleep(poll_interval)
            elapsed += poll_interval
            data = self._get(RECORD_URL, params={"taskId": task_id}, label="recordInfo")["data"]
            state = data.get("state")
            print(f"  → [{elapsed}s] state: {state}")
            if state == "success":
                self.total_credits += data.get("creditsConsumed") or 0
                self.total_cost += COST_PER_IMAGE.get((model, resolution.lower()), 0)
                result = json.loads(data["resultJson"])
                return result["resultUrls"][0]
            if state == "fail":
                raise RuntimeError(f"Generation failed: {data.get('failCode')} {data.get('failMsg')}")

        raise TimeoutError(f"Generation timed out after {max_wait}s — task {task_id}")

    def download(self, image_url: str, save_path: str | Path) -> Path:
        """Download generated image to disk, retrying on transient network errors."""
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(1, 4):
            try:
                resp = requests.get(image_url, timeout=180)
                resp.raise_for_status()
                save_path.write_bytes(resp.content)
                return save_path
            except Exception as exc:
                if attempt == 3:
                    raise
                print(f"  → download attempt {attempt} failed ({exc.__class__.__name__}) — retrying")
                time.sleep(3 * attempt)
        return save_path

    def credit_balance(self) -> int:
        """Return the account's remaining credit balance."""
        return self._get(CREDIT_URL, label="credit")["data"]

    # -- internals -----------------------------------------------------------

    def _to_url(self, img: str) -> str:
        """Pass through an existing URL; upload a local file and return its temp URL."""
        p = Path(img)
        if not p.exists():
            return img  # already a URL
        data = base64.b64encode(p.read_bytes()).decode()
        suffix = p.suffix.lstrip(".").lower()
        mime = "image/png" if suffix == "png" else "image/jpeg"
        payload = {
            "base64Data": f"data:{mime};base64,{data}",
            "uploadPath": "images/slides-refs",
            "fileName": p.name,
        }
        for attempt in range(1, 4):
            try:
                resp = self.session.post(UPLOAD_URL, json=payload, timeout=120)
                resp.raise_for_status()
                break
            except Exception as exc:
                if attempt == 3:
                    raise
                print(f"  → upload attempt {attempt} failed ({exc.__class__.__name__}) — retrying")
                time.sleep(3 * attempt)
        url = resp.json()["data"]["downloadUrl"]
        print(f"  → uploaded {p.name} → {url}")
        return url

    def _post(self, url: str, payload: dict, label: str) -> dict:
        for attempt in range(1, 4):
            try:
                resp = self.session.post(url, json=payload, timeout=120)
                break
            except Exception as exc:
                if attempt == 3:
                    raise
                print(f"  → {label} POST attempt {attempt} failed ({exc.__class__.__name__}) — retrying")
                time.sleep(3 * attempt)
        resp.raise_for_status()
        body = resp.json()
        if body.get("code") not in (200, None):
            raise RuntimeError(f"{label} error {body.get('code')}: {body.get('msg')}")
        return body

    def _get(self, url: str, label: str, params: dict | None = None) -> dict:
        for attempt in range(1, 4):
            try:
                resp = self.session.get(url, params=params, timeout=30)
                break
            except Exception as exc:
                if attempt == 3:
                    raise
                print(f"  → {label} GET attempt {attempt} failed ({exc.__class__.__name__}) — retrying")
                time.sleep(3 * attempt)
        resp.raise_for_status()
        return resp.json()
