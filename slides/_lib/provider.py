"""
Image-provider selection for the slides pipeline.

Both clients (KieClient, WaveSpeedClient) expose the same interface:
  generate(prompt, mode, model, images, aspect_ratio, resolution, ...) -> url
  download(url, path) -> Path
  total_cost  (float)

Provider precedence (first match wins):
  1. --provider <name> on the command line
  2. "provider" field in the project's project.json
  3. IMAGE_PROVIDER env var
  4. default: "kie"
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
    raise ValueError(f"Unknown image provider: {provider!r} (expected 'kie' or 'wavespeed')")
