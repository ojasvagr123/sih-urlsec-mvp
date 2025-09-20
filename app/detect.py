import re
from typing import Tuple, Optional, Dict, Any
from .utils import char_entropy, count_specials
from .typosquat import typosquat_score

SIG = {
    "sql_injection": re.compile(r"(?i)(union\s+select|or\s+1=1|;--|drop\s+table|sleep\()"),
    "xss": re.compile(r"(?i)(<\s*script|onerror\s*=|onload\s*=|document\.cookie|javascript:)"),
    "dir_traversal": re.compile(r"(\.\./|%2e%2e%2f|%2e%2e/)"),
    "cmd_injection": re.compile(r"(;|&&|\|\||`|\$\(.*\))"),
    "ssrf": re.compile(r"(?i)(http|file|gopher|dict|smb|ftp)://(127\.0\.0\.1|localhost|169\.254\.|10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"),
    "lfi_rfi": re.compile(r"(?i)(file://|php://|expect://|data:text|\.{2}/etc/passwd)"),
    "http_param_poll": re.compile(r"(&|\?)\w+=.*(&|&.*\b\w+=)"),
    "xxe": re.compile(r"(?s)<!ENTITY\s+\w+\s+SYSTEM\s+\"[^\"]+\""),
    "webshell_upload": re.compile(r"(?i)\.(jsp|asp|aspx|php|phtml)(\?|$)")
}

def analyze(event: Dict[str, Any]) -> Tuple[Optional[str], float]:
    url = event.get("url") or ""
    params = event.get("params") or {}
    headers = event.get("headers") or {}
    body = event.get("body_snippet") or ""
    haystack = " ".join([url, str(params), str(headers), str(body)])

    for atype, rx in SIG.items():
        if rx.search(haystack):
            conf = 0.95 if atype != "http_param_poll" else 0.8
            return atype, conf

    special_cnt = count_specials(haystack)
    ent = char_entropy(haystack)
    if special_cnt > 8 and ent > 3.8:
        return "suspicious_payload", 0.65

    host_or_url = headers.get("Host") or headers.get("host") or url
    try:
        ts = typosquat_score(host_or_url)
        if ts <= 1:
            return "typosquatting", 0.7
    except Exception:
        pass

    return None, 0.0
