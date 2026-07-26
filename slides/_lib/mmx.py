"""
mmx CLI wrapper for image generation.

Shells out to the locally-installed `mmx` CLI (image-01 / image-01-live) instead
of calling kie.ai or WaveSpeed. Mirrors the KieClient / WaveSpeedClient interface
(generate / download / total_cost) so the pipeline can swap providers without
other code changes. See slides/_lib/provider.py.

Why a CLI wrapper instead of a direct HTTP client?
  - `mmx` handles auth, base64 uploads, polling, and CDN fetch for us
  - One less SDK / API surface to maintain
  - Falls under MiniMax's own billing/quotas, so no per-image $ cost — quota only

Differences from the kie.ai / WaveSpeed flow:
  - mmx writes the output image directly to a file path you specify via --out.
    So `generate()` returns a local path, and `download()` is just a move.
  - mmx's only resolution knob is --width / --height (max 2048). We map
    "1k" / "2k" / "4k" to 1024 / 1536 / 2048.
  - mmx's subject-reference is a single --subject-ref flag per call. We pass
    the first character ref and warn if there are more (kie/wavespeed can take
    up to 14; if you need multi-ref consistency, fall back to --provider kie).
  - No cost in dollars; quota only. We track `total_cost = 0.0` for interface
    parity and `total_quota_calls` for sanity.
"""
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


# mmx image-01 is the current model. We also accept the kie / wavespeed model
# names ("nano-banana-pro", "nano-banana-2") as aliases so scenes.json can
# stay provider-agnostic — anything kie/wavespeed supports maps to image-01.
SUPPORTED_MODELS = {"image-01", "image-01-live", "nano-banana-pro", "nano-banana-2"}
# But only "image-*" actually exist on mmx — everything else gets aliased.
_MMX_MODEL_ALIAS = {
    "nano-banana-pro": "image-01",
    "nano-banana-2":   "image-01",
}

# Known aspect ratios mmx accepts. We pass through whatever the caller asks for
# (mmx will reject nonsense values), but warn if it's outside this set.
KNOWN_ASPECT_RATIOS = {
    "1:1", "16:9", "9:16", "4:3", "3:4", "16:10", "10:16",
    "2:3", "3:2", "21:9", "9:21",
}

# mmx --width / --height range (from the CLI help). 2048 is the upper bound.
_MMX_MAX_EDGE = 2048
_MMX_MIN_EDGE = 512

# Mode mapping. mmx doesn't have an explicit edit/text-to-image mode — it
# infers from whether --subject-ref is passed. The pipeline's `mode` field
# still controls this.
_EDIT_MODES = {"edit", "edit-fast", "edit-ultra"}


# ---------------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------------

def mmx_available() -> bool:
    """True if the `mmx` CLI is on PATH and responds to --version."""
    try:
        out = subprocess.run(
            ["mmx", "--version"], capture_output=True, text=True, timeout=5,
        )
        return out.returncode == 0
    except Exception:
        return False


def mmx_auth_ok() -> bool:
    """True if mmx has a working API key configured (login or env)."""
    if not mmx_available():
        return False
    try:
        out = subprocess.run(
            ["mmx", "auth", "status", "--output", "json"],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode != 0:
            return False
        body = json.loads(out.stdout)
        return body.get("method") in ("api-key", "oauth")
    except Exception:
        return False


def mmx_quota() -> dict:
    """Return the raw `mmx quota show` JSON for diagnostics."""
    try:
        out = subprocess.run(
            ["mmx", "quota", "show", "--output", "json"],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode != 0:
            return {"error": out.stderr.strip() or "mmx quota show failed"}
        return json.loads(out.stdout)
    except Exception as exc:
        return {"error": str(exc)}


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class MmxClient:
    name = "mmx"

    def __init__(self):
        if not mmx_available():
            raise RuntimeError(
                "mmx CLI not found on PATH. Install from "
                "https://github.com/anthropics/mmx-cli (or `brew install mmx`), "
                "then run `mmx auth login`."
            )
        if not mmx_auth_ok():
            raise RuntimeError(
                "mmx auth not configured. Run `mmx auth login` (or set MMX_API_KEY), "
                "then retry."
            )

        self.total_cost = 0.0          # interface parity with kie/wavespeed (always 0)
        self.total_quota_calls = 0     # how many generations we've made this run

    # -- public interface (matches KieClient / WaveSpeedClient) ---------------

    def generate(
        self,
        prompt: str,
        mode: str = "text-to-image",
        model: str = "image-01",
        images: list[str] | None = None,
        aspect_ratio: str = "16:9",
        resolution: str = "2k",
        output_format: str = "png",
        poll_interval: int = 5,        # unused, accepted for interface parity
        max_wait: int = 300,
        seed: int | None = None,
    ) -> str:
        """Submit a generation request via mmx CLI. Returns the local path of
        a temp file containing the generated image. The caller should follow
        up with `download(temp_path, final_path)` to move it into place.

        `mode` is accepted for interface parity — mmx's image-01 infers
        edit-vs-text-to-image from whether --subject-ref is passed.
        `resolution` is mapped to mmx's --width/--height (max 2048).
        """
        if model not in SUPPORTED_MODELS:
            raise ValueError(
                f"mmx: unsupported model {model!r} (expected one of {sorted(SUPPORTED_MODELS)})"
            )
        # Translate kie / wavespeed model names to mmx's actual model.
        actual_model = _MMX_MODEL_ALIAS.get(model, model)

        if aspect_ratio not in KNOWN_ASPECT_RATIOS:
            print(f"  [WARN] mmx: aspect-ratio {aspect_ratio!r} not in known set, passing through")

        # mmx writes directly to a file. We use a temp file because the existing
        # call pattern is generate(url) -> download(url, final_path), and we
        # want to keep that contract for all providers.
        tmp = tempfile.NamedTemporaryFile(
            prefix="mmx-", suffix=f".{output_format}", delete=False
        )
        tmp_path = Path(tmp.name)
        tmp.close()

        cmd = [
            "mmx", "image", "generate",
            "--prompt", prompt,
            "--aspect-ratio", aspect_ratio,
            "--out", str(tmp_path),
            "--non-interactive",
        ]

        # Resolution mapping. mmx has no 1k/2k/4k concept — it takes width/height
        # in px, AND requires both (--width requires --height per the CLI).
        wh = self._resolve_dimensions(resolution, aspect_ratio)
        if wh is not None:
            cmd += ["--width", str(wh[0]), "--height", str(wh[1])]

        if seed is not None:
            cmd += ["--seed", str(seed)]

        # Edit mode → pass refs via --subject-ref. mmx accepts a single
        # --subject-ref per call (verified via the CLI help), so we pass
        # the first ref and warn if the scene had more.
        refs_to_pass = []
        if mode in _EDIT_MODES and images:
            for img in images:
                p = Path(img)
                if p.exists():
                    refs_to_pass.append(p)
            if len(refs_to_pass) > 1:
                print(
                    f"  [WARN] mmx --subject-ref takes a single image; "
                    f"passing the first of {len(refs_to_pass)} refs "
                    f"({refs_to_pass[0].name}). For multi-ref consistency, "
                    f"use --provider kie or --provider wavespeed."
                )

        if refs_to_pass:
            cmd += ["--subject-ref", f"type=character,image={refs_to_pass[0]}"]

        print(
            f"  → mmx image generate "
            f"(model={actual_model}, mode={mode}, aspect={aspect_ratio}, "
            f"ref={refs_to_pass[0].name if refs_to_pass else 'none'})"
        )

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=max_wait)
        except subprocess.TimeoutExpired:
            tmp_path.unlink(missing_ok=True)
            raise TimeoutError(f"mmx image generate timed out after {max_wait}s")

        if result.returncode != 0:
            err = (result.stderr or result.stdout or "unknown error").strip()
            tmp_path.unlink(missing_ok=True)
            raise RuntimeError(f"mmx image generate failed (exit {result.returncode}): {err}")

        if not tmp_path.exists() or tmp_path.stat().st_size == 0:
            tmp_path.unlink(missing_ok=True)
            raise RuntimeError(f"mmx image generate produced no file at {tmp_path}")

        self.total_quota_calls += 1
        # Return the local path. The pipeline will call download() to move it.
        return str(tmp_path)

    def download(self, image_url: str, save_path: str | Path) -> Path:
        """For mmx, the 'url' is actually a temp file path written by --out.
        Just move it into place."""
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        src = Path(image_url)
        if not src.exists():
            raise FileNotFoundError(f"mmx temp file missing: {src}")
        shutil.move(str(src), str(save_path))
        return save_path

    def credit_balance(self) -> dict:
        """Return mmx quota info as a dict (analogue of kie.credit_balance)."""
        return mmx_quota()

    # -- internals ----------------------------------------------------------

    def _resolve_dimensions(self, resolution: str, aspect_ratio: str) -> tuple[int, int] | None:
        """Map '1k' / '2k' / '4k' to (width, height) px that mmx accepts.
        Returns None to let mmx pick its own default (no --width/--height).
        Both dimensions are multiples of 8 and within mmx's [512, 2048] range.
        """
        table = {"1k": 1024, "2k": 1536, "4k": 2048}
        target_short = table.get((resolution or "").lower())
        if target_short is None:
            return None
        target_short = max(_MMX_MIN_EDGE, min(_MMX_MAX_EDGE, target_short))

        # Parse aspect ratio. Default to 1:1 if unparseable.
        try:
            w_ratio, h_ratio = (int(x) for x in aspect_ratio.split(":"))
        except (ValueError, AttributeError):
            w_ratio, h_ratio = 1, 1

        # Pick the orientation that fits target_short on the longer edge.
        if w_ratio >= h_ratio:
            w = target_short
            h = max(_MMX_MIN_EDGE, int(round(w * h_ratio / w_ratio)))
        else:
            h = target_short
            w = max(_MMX_MIN_EDGE, int(round(h * w_ratio / h_ratio)))

        # Clamp + snap to multiples of 8 (mmx requires).
        w = max(_MMX_MIN_EDGE, min(_MMX_MAX_EDGE, w - (w % 8)))
        h = max(_MMX_MIN_EDGE, min(_MMX_MAX_EDGE, h - (h % 8)))
        return w, h
