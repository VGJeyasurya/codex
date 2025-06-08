import argparse
import json
import logging
from pathlib import Path
from typing import List

from .modules import (
    subdomain_enum,
    port_scanner,
    service_enum,
    whois_lookup,
    dns_lookup,
    web_crawler,
)


logger = logging.getLogger(__name__)


def setup_logging(verbose: bool, log_file: Path):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Python Recon Tool")
    parser.add_argument("target", help="Target domain or IP")
    parser.add_argument("--ports", help="Comma separated list of ports for scanning", default="1-1024")
    parser.add_argument("--subdomains", action="store_true", help="Enumerate subdomains")
    parser.add_argument("--scan", action="store_true", help="Perform port scan")
    parser.add_argument("--services", action="store_true", help="Detect services on open ports")
    parser.add_argument("--whois", action="store_true", help="Perform WHOIS lookup")
    parser.add_argument("--dns", action="store_true", help="Lookup DNS records")
    parser.add_argument("--reverse", action="store_true", help="Reverse DNS lookup (for IP)")
    parser.add_argument("--crawl", action="store_true", help="Web crawl target")
    parser.add_argument("--output", help="Output prefix", default="output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    return parser.parse_args()


def parse_port_range(port_str: str) -> List[int]:
    ports = []
    for part in port_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return ports


def main():
    args = parse_args()
    log_file = Path(f"{args.output}.log")
    setup_logging(args.verbose, log_file)

    results = {}

    if args.subdomains:
        logger.info("Enumerating subdomains")
        subs = subdomain_enum.enumerate_subdomains(args.target)
        results['subdomains'] = subs
        logger.info("Found %d subdomains", len(subs))

    port_results = {}
    if args.scan or args.services:
        ports = parse_port_range(args.ports)
        logger.info("Scanning ports: %s", ports)
        port_results = port_scanner.scan_ports(args.target, ports)
        results['ports'] = port_results

    if args.services and port_results:
        logger.info("Detecting services")
        services = service_enum.detect_services(port_results)
        results['services'] = services

    if args.whois:
        logger.info("Performing WHOIS lookup")
        results['whois'] = whois_lookup.perform_whois(args.target)

    if args.dns:
        logger.info("Looking up DNS records")
        results['dns'] = dns_lookup.lookup_records(args.target)

    if args.reverse:
        logger.info("Performing reverse DNS lookup")
        results['reverse'] = dns_lookup.reverse_lookup(args.target)

    if args.crawl:
        logger.info("Crawling website")
        start_url = f"http://{args.target}" if not args.target.startswith("http") else args.target
        results['crawl'] = web_crawler.crawl(start_url)

    json_file = Path(f"{args.output}.json")
    with open(json_file, 'w') as jf:
        json.dump(results, jf, indent=2)
    text_file = Path(f"{args.output}.txt")
    with open(text_file, 'w') as tf:
        for key, value in results.items():
            tf.write(f"{key}: {value}\n")

    logger.info("Results saved to %s and %s", json_file, text_file)


if __name__ == "__main__":
    main()
