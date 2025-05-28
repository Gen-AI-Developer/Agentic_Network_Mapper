import nmap

def scan_ip_for_open_ports(ip_address: str, port_range: str = '1-1024') -> list:
    """
    Scan the given IP address for open ports within the specified port range.

    :param ip_address: The target IP address to scan.
    :param port_range: The range of ports to scan, e.g., '1-1024' or '22,80,443'.
    :return: A list of open ports.
    """
    nm = nmap.PortScanner()
    try:
        print(f"LOG: Scanning {ip_address} for open ports in range {port_range}")
        # Changed from -sS to -sT for non-root TCP connect scan
        nm.scan(ip_address, port_range, arguments='-sT')

        open_ports = []
        if ip_address in nm.all_hosts():
            for proto in nm[ip_address].all_protocols():
                lport = nm[ip_address][proto].keys()
                for port in sorted(lport):
                    state = nm[ip_address][proto][port]['state']
                    if state == 'open':
                        open_ports.append(port)

        print(f"LOG: Open ports on {ip_address}: {open_ports}")
        return open_ports

    except Exception as e:
        print(f"LOG: Error scanning {ip_address}: {e}")
        return []


import nmap

def scan_for_port_services(ip_address: str, ports: list[int]) -> dict:
    """
    Scan an IP address for a list of ports and return a dictionary of open ports and their services.
    """
    nm = nmap.PortScanner()
    try:
        port_str = ','.join(str(p) for p in ports)
        print(f"LOG: Scanning IP address {ip_address} for ports: {port_str}")
        
        # Changed from -sS to -sT for non-root TCP connect scan
        nm.scan(ip_address, port_str, arguments='-sT -v')

        services = {}
        if ip_address in nm.all_hosts():
            for port in ports:
                if nm[ip_address].has_tcp(port):
                    port_info = nm[ip_address]['tcp'][port]
                    if port_info['state'] == 'open':
                        service_name = port_info.get('name', 'unknown')
                        services[port] = service_name
                        print(f"LOG: Service on {ip_address}:{port} is {service_name}")
                    else:
                        print(f"LOG: Port {port} is not open.")
                else:
                    print(f"LOG: No TCP info for port {port}")
        return services

    except Exception as e:
        print(f"LOG: Error scanning {ip_address} ports {ports}: {e}")
        return {}
