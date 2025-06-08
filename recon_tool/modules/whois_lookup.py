import whois
from typing import Dict


def perform_whois(domain: str) -> Dict:
    """Return WHOIS information for the given domain."""
    try:
        w = whois.whois(domain)
        return dict(w)
    except Exception:
        return {}
