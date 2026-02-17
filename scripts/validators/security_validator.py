"""Security scanning helpers for workflows.

Provides small functions used by pytest to ensure Phase 1 sanitization remains effective
(e.g. no hard-coded emails, VPS URLs, raw credential/instance/webhook IDs in workflow JSON).
"""
from pathlib import Path
import re
from typing import List, Dict, Any

# Patterns
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Only flag known private/internal hosts (not public docs n8n.io)
_VPS_RE = re.compile(r"(srv830801\.hstgr\.cloud|hstgr\.cloud|n8n\.srv)", re.I)

# Credential-like IDs should be detected in JSON `credentials.*.id` fields only
_CRED_ID_RE = re.compile(r"^[A-Za-z0-9]{16}$")

# Instance and webhook IDs are detected by JSON key names (UUID/hex patterns kept as validators)
_INSTANCE_ID_RE = re.compile(r"^[a-f0-9]{64}$", re.I)
_WEBHOOK_ID_RE = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", re.I)

# Domains that are allowed in examples
_EXEMPT_EMAIL_DOMAINS = {"example.com", "example.org", "example.net", "localhost"}


def _json_files(root: Path) -> List[Path]:
    if not root.exists():
        return []
    return [p for p in root.rglob("*.json") if p.is_file()]


def _read_text_safe(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def find_emails_in_workflows(workflows_path: str = "workflows") -> List[Dict[str, Any]]:
    """Return list of {file, email} for non-exempt emails found in workflow JSON files."""
    root = Path(workflows_path)
    results: List[Dict[str, Any]] = []

    for p in _json_files(root):
        text = _read_text_safe(p)
        for m in _EMAIL_RE.finditer(text):
            email = m.group(0)
            domain = email.split("@", 1)[-1].lower()
            if domain in _EXEMPT_EMAIL_DOMAINS:
                continue
            # ignore placeholder 'your-email@example.com' (example.com is exempt)
            results.append({"file": str(p), "email": email})
    return results


def find_vps_urls_in_workflows(workflows_path: str = "workflows") -> List[Dict[str, Any]]:
    root = Path(workflows_path)
    results: List[Dict[str, Any]] = []
    for p in _json_files(root):
        text = _read_text_safe(p)
        for m in _VPS_RE.finditer(text):
            results.append({"file": str(p), "url": m.group(0)})
    return results


def find_credential_like_ids_in_workflows(workflows_path: str = "workflows") -> List[Dict[str, Any]]:
    """Find credential-like IDs only inside `credentials.*.id` fields by parsing JSON.

    This avoids false positives from node ids, property names, or other 16-char tokens.
    """
    import json

    root = Path(workflows_path)
    results: List[Dict[str, Any]] = []

    for p in _json_files(root):
        text = _read_text_safe(p)
        try:
            data = json.loads(text)
        except Exception:
            continue

        def _walk(obj):
            if isinstance(obj, dict):
                # credentials dict is where credential IDs live
                if 'credentials' in obj and isinstance(obj['credentials'], dict):
                    for cred_type, cred_val in obj['credentials'].items():
                        if isinstance(cred_val, dict) and 'id' in cred_val:
                            cid = cred_val.get('id')
                            if isinstance(cid, str) and _CRED_ID_RE.match(cid) and not cid.startswith('CRED_'):
                                results.append({"file": str(p), "credential_field": cred_type, "id": cid})
                for v in obj.values():
                    _walk(v)
            elif isinstance(obj, list):
                for item in obj:
                    _walk(item)

        _walk(data)
    return results


def find_instance_ids_in_workflows(workflows_path: str = "workflows") -> List[Dict[str, Any]]:
    """Find JSON keys named `instanceId` (exact key match) to avoid false positives."""
    import json
    root = Path(workflows_path)
    results: List[Dict[str, Any]] = []

    for p in _json_files(root):
        text = _read_text_safe(p)
        try:
            data = json.loads(text)
        except Exception:
            continue

        def _walk(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == 'instanceId' and isinstance(v, str) and _INSTANCE_ID_RE.match(v):
                        results.append({"file": str(p), "instanceId": v})
                    _walk(v)
            elif isinstance(obj, list):
                for item in obj:
                    _walk(item)

        _walk(data)
    return results


def find_webhook_ids_in_workflows(workflows_path: str = "workflows") -> List[Dict[str, Any]]:
    """Find JSON keys named `webhookId` (exact key match) to avoid flagging UUIDs used for nodes."""
    import json
    root = Path(workflows_path)
    results: List[Dict[str, Any]] = []

    for p in _json_files(root):
        text = _read_text_safe(p)
        try:
            data = json.loads(text)
        except Exception:
            continue

        def _walk(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == 'webhookId' and isinstance(v, str) and _WEBHOOK_ID_RE.match(v):
                        results.append({"file": str(p), "webhookId": v})
                    _walk(v)
            elif isinstance(obj, list):
                for item in obj:
                    _walk(item)

        _walk(data)
    return results


def run_quick_scan(workflows_path: str = "workflows") -> Dict[str, Any]:
    return {
        "emails": find_emails_in_workflows(workflows_path),
        "vps_urls": find_vps_urls_in_workflows(workflows_path),
        "credential_like_ids": find_credential_like_ids_in_workflows(workflows_path),
        "instance_ids": find_instance_ids_in_workflows(workflows_path),
        "webhook_ids": find_webhook_ids_in_workflows(workflows_path),
    }


if __name__ == "__main__":
    import json
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "workflows"
    print(json.dumps(run_quick_scan(path), indent=2))
