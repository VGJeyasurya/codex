import dns.resolver
from typing import Dict, List


RECORD_TYPES = ["A", "MX", "TXT", "NS"]


def lookup_records(domain: str, record_types: List[str] = None) -> Dict[str, List[str]]:
    """Lookup DNS records for the given domain."""
    if record_types is None:
        record_types = RECORD_TYPES

    results = {}
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            results[rtype] = [rdata.to_text() for rdata in answers]
        except Exception:
            results[rtype] = []
    return results


def reverse_lookup(ip: str) -> str:
    """Perform reverse DNS lookup for an IP address."""
    try:
        addr = dns.reversename.from_address(ip)
        return str(dns.resolver.resolve(addr, "PTR")[0])
    except Exception:
        return ""
