#!/usr/bin/env python3
"""Use selected library references with xAI Responses; no local tools are executed."""

import argparse
import json
import math
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from portable_skills import ROOT, CHAT_GUIDANCE, context_markdown, selection


ENDPOINT = "https://api.x.ai/v1/responses"
MAX_RESPONSE_BYTES = 8 * 1024 * 1024


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def payload(root, names, model, prompt, max_output_tokens=4096):
    if not model.strip() or not prompt.strip():
        raise ValueError("Model and prompt must not be empty")
    if max_output_tokens <= 0:
        raise ValueError("max-output-tokens must be positive")
    pins = selection(root, names)
    context = "\n\n".join(context_markdown(root, name, pin) for name, pin in pins.items())
    return {"model": model, "store": False, "stream": False,
            "max_output_tokens": max_output_tokens,
            "input": [{"role": "system", "content": CHAT_GUIDANCE + "\n\n" + context},
                      {"role": "user", "content": prompt}]}


def send(body, api_key, timeout=120):
    if not api_key or not api_key.strip():
        raise ValueError("Set XAI_API_KEY in your environment; never put the key in a prompt or repository")
    if not api_key.isascii() or any(ord(c) < 33 or ord(c) > 126 for c in api_key):
        raise ValueError("XAI_API_KEY must be a single ASCII token without whitespace")
    if not math.isfinite(timeout) or not 0 < timeout <= 3600:
        raise ValueError("timeout must be between 0 and 3600 seconds")
    request = Request(ENDPOINT, data=json.dumps(body).encode(), method="POST",
                      headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"})
    # One bounded request. No automatic retries or redirected credential forwarding.
    try:
        with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
            data = response.read(MAX_RESPONSE_BYTES + 1)
    except HTTPError as error:
        code = error.code
        error.close()
        raise RuntimeError(f"xAI HTTP {code}; check account/model access or rate limits. Request was not retried.") from None
    except (URLError, TimeoutError) as error:
        raise RuntimeError("xAI connection failed or timed out; delivery may be uncertain. Request was not retried.") from None
    if len(data) > MAX_RESPONSE_BYTES:
        raise RuntimeError("xAI response exceeded the local size limit")
    try:
        result = json.loads(data)
        if result.get("status") != "completed":
            raise ValueError("Response is incomplete or failed; inspect model output limits before making another request")
        text = "\n".join(part["text"] for item in result.get("output", [])
                         if item.get("type") == "message"
                         for part in item.get("content", []) if part.get("type") == "output_text")
        if not text.strip():
            raise ValueError("Response contains no completed output text")
        return {"id": result.get("id"), "model": result.get("model", body["model"]),
                "status": "completed", "text": text, "usage": result.get("usage")}
    except (TypeError, AttributeError, KeyError, UnicodeError, ValueError) as error:
        raise RuntimeError("xAI did not return completed response text; check response format or output limits") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", action="append", required=True, help="Select relevant skills explicitly; repeat for more than one")
    parser.add_argument("--model", required=True, help="A Responses-compatible model available to your xAI account")
    parser.add_argument("--prompt-file", type=Path, required=True, help="UTF-8 task text; only this file and selected skills are sent")
    parser.add_argument("--max-output-tokens", type=int, default=4096)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--dry-run", action="store_true", help="Print the exact request without network access or an API key")
    args = parser.parse_args()
    try:
        body = payload(ROOT, args.skill, args.model, args.prompt_file.read_text(encoding="utf-8"), args.max_output_tokens)
        result = body if args.dry_run else send(body, os.environ.get("XAI_API_KEY"), args.timeout)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Grok request: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
