# Python Recon Tool

This project provides a modular reconnaissance tool for penetration testing. It supports subdomain enumeration, port scanning, service detection, WHOIS lookup, DNS queries, reverse DNS lookups, and basic web crawling.

## Requirements

- Python 3.8+
- Packages: `requests`, `python-whois`, `dnspython`, `beautifulsoup4`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m recon_tool.main example.com --subdomains --scan --whois --dns
```

Results are stored in JSON and text files prefixed with `output` by default.
