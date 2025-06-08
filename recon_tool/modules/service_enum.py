from typing import Dict

DEFAULT_SERVICES = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    443: "https",
}


def detect_services(port_banners: Dict[int, str]) -> Dict[int, str]:
    """Basic service detection based on port numbers and banner contents."""
    services = {}
    for port, banner in port_banners.items():
        service = DEFAULT_SERVICES.get(port, "unknown")
        if "http" in banner.lower():
            service = "http"
        elif "ssh" in banner.lower():
            service = "ssh"
        elif "smtp" in banner.lower():
            service = "smtp"
        services[port] = service
    return services
