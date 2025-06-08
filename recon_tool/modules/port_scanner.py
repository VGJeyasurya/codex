import socket
from typing import Dict, List


def scan_ports(target: str, ports: List[int]) -> Dict[int, str]:
    """Scan a list of TCP ports on the target. Returns banner string for open ports."""
    results = {}
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                if sock.connect_ex((target, port)) == 0:
                    try:
                        sock.sendall(b"\r\n")
                        banner = sock.recv(1024).decode(errors="ignore").strip()
                    except Exception:
                        banner = "open"
                    results[port] = banner
        except Exception:
            continue
    return results
