"""
Image-provider selection for the slides pipeline.

All clients (KieClient, WaveSpeedClient, MmxClient) expose the same interface:
  generate(prompt, mode, model, images, aspect_ratio, resolution, ...) -> url | path
  download(url, path) -> Path
  total_cost  (float, 0 for mmx — quota only)

Provider precedence (first match wins):
  1. --provider <name> on the command line
  2. "provider" field in the project's project.json
  3. IMAGE_PROVIDER env var
  4. default: "kie"

Available providers:
  kie        — kie.ai API (default). Bills in credits; has KIE_API_KEY in .env.
  wavespeed  — WaveSpeed API. Bills per image; has WAVESPEEDAI_API_KEY in .env.
  mmx        — local `mmx` CLI. Quota only (no per-image $), uses `mmx auth login`.
               Subject-ref only takes a single image per call — for multi-ref
               consistency, fall back to kie/wavespeed.

NOTE on the agent's preferred default:
  When the agent (Mavis) generates images conversationally, the preferred path
  is the built-in `image_synthesize` tool (no API key, no quota, no install).
  This module only covers the script-driven path (generate_characters.py /
  generate_scenes.py), which always shells out to a CLI / HTTP client. Set
  IMAGE_PROVIDER=mmx in .env (or pass --provider mmx) for the closest
  no-API-key script path.
"""
import json
import os
from pathlib import Path


DEFAULT_PROVIDER = "kie"


def resolve_provider(cli_provider: str | None = None, project: Path | None = None) -> str:
    if cli_provider:
        return cli_provider.lower()
    if project is not None:
        cfg = project / "project.json"
        if cfg.exists():
            p = json.loads(cfg.read_text()).get("provider")
            if p:
                return p.lower()
    return os.environ.get("IMAGE_PROVIDER", DEFAULT_PROVIDER).lower()


def get_client(provider: str):
    if provider == "wavespeed":
        from wavespeed import WaveSpeedClient
        return WaveSpeedClient()
    if provider == "kie":
        from kie import KieClient
        return KieClient()
    if provider == "mmx":
        from mmx import MmxClient
        return MmxClient()
    raise ValueError(
        f"Unknown image provider: {provider!r} "
        f"(expected 'kie', 'wavespeed', or 'mmx')"
    )


def list_providers() -> list[str]:
    """Return the names of all providers known to the pipeline."""
    return ["kie", "wavespeed", "mmx"]
