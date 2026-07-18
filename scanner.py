import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 5432, 6379, 8080]

def scan_port(host: str, port: int, timeout: float = 0.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port, "tcp")
                except OSError:
                    service = "unknown"
                return port, service
    except OSError:
        pass
    return None

def scan_ports(host: str, ports, workers: int = 100, timeout: float = 0.5):
    open_ports = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(scan_port, host, port, timeout) for port in ports]
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
    return sorted(open_ports, key=lambda x: x[0])

def parse_args():
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("host", help="Target IP or hostname")
    parser.add_argument("--start", type=int, default=1, help="Start port")
    parser.add_argument("--end", type=int, default=1024, help="End port")
    parser.add_argument("--common", action="store_true", help="Scan common ports only")
    parser.add_argument("--timeout", type=float, default=0.5, help="Socket timeout in seconds")
    parser.add_argument("--workers", type=int, default=100, help="Number of threads")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.common:
        ports = COMMON_PORTS
    else:
        ports = range(args.start, args.end + 1)

    print(f"Scanning {args.host}...")
    open_ports = scan_ports(args.host, ports, workers=args.workers, timeout=args.timeout)

    if not open_ports:
        print("No open ports found.")
        return

    print("Open ports:")
    for port, service in open_ports:
        print(f"{port}/tcp - {service}")

if __name__ == "__main__":
    main()