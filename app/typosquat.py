from Levenshtein import distance as lev
import tldextract

def typosquat_score(url_or_host: str, protected_domains=None):
    if protected_domains is None:
        protected_domains = ["example.com", "login.gov.in", "mybank.in", "securepay.in"]
    host = url_or_host
    if "://" in url_or_host:
        import urllib.parse as up
        host = up.urlparse(url_or_host).netloc
    ext = tldextract.extract(host)
    domain = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
    return min(lev(domain, pd) for pd in protected_domains)
