# Python Port Scanner

A simple TCP port scanner for checking open ports on hosts you own or are authorized to test.

## Features
- Scan a custom range of ports.
- Scan common ports only.
- Identify service names for known ports.
- Multithreaded scanning for speed.

## Usage

### Scan common ports
```bash
python scanner.py 127.0.0.1 --common
```

### Scan a port range
```bash
python scanner.py 127.0.0.1 --start 1 --end 1024
```

### Adjust timeout and threads
```bash
python scanner.py 127.0.0.1 --common --timeout 1.0 --workers 200
```

## Testing
```bash
pytest -q
```

## Safety
Use only on systems you own or have explicit permission to test.
