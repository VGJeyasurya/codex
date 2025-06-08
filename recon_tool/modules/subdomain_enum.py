import requests
import dns.resolver
from typing import List


def enumerate_subdomains(domain: str) -> List[str]:
    """Enumerate subdomains for a given domain using crt.sh and DNS queries."""
    discovered = set()

    # Use crt.sh to find subdomains via certificate transparency logs
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp = requests.get(url, timeout=10)
        if resp.ok:
            for entry in resp.json():
                name_value = entry.get("name_value", "")
                for sub in name_value.split("\n"):
                    if sub.endswith(domain):
                        discovered.add(sub.strip())
    except Exception:
        pass

    # Attempt DNS zone transfer for common nameservers
    common_ns = [f"ns{i}.{domain}" for i in range(1, 5)]
    for ns in common_ns:
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            for rdata in answers:
                try:
                    zone = dns.resolver.zone_for_name(domain, relativize=False)
                    for name, node in zone.nodes.items():
                        subdomain = f"{name}.{domain}"
                        discovered.add(subdomain)
                except Exception:
                    break
        except Exception:
            break

    return sorted(discovered)
