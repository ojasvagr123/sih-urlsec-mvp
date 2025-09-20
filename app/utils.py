import uuid, re
from urllib.parse import urlparse, parse_qs

def gen_event_id():
    return str(uuid.uuid4())

def safe_parse_url(url_str: str):
    try:
        return urlparse(url_str)
    except Exception:
        return urlparse("http://dummy" + (url_str if url_str.startswith('/') else "/" + url_str))

def extract_params(url_str: str):
    u = safe_parse_url(url_str)
    q = parse_qs(u.query)
    return {k: (v[0] if isinstance(v, list) and len(v)==1 else v) for k,v in q.items()}

def char_entropy(s: str):
    if not s: return 0.0
    from math import log2
    from collections import Counter
    c = Counter(s); n = len(s)
    return -sum((cnt/n)*log2(cnt/n) for cnt in c.values())

def count_specials(s: str):
    if not s: return 0
    return len(re.findall(r"[%#<>'\";`|&]", s))

def to_snippet(body: str, n=200):
    if not body: return None
    return str(body)[:n]
