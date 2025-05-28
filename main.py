from fastapi import FastAPI, Path
from pydantic import BaseModel, IPvAnyAddress, ValidationError
from typing import Union, List

from network_mapper.nmap_core import scan_for_port_services, scan_ip_for_open_ports  # Assuming this function is defined in network_mapper.py

app = FastAPI()

class NetworkScan(BaseModel):
    network_id: IPvAnyAddress

@app.get("/")
async def read_root():
    print("LOG: Welcome to the Agentic Network Mapper API!")
    return {"message": "Welcome to the Agentic Network Mapper API!"}

def verify_ip_address(network_id: str) -> bool:
    """
    Verify if the provided network ID is a valid IP address using Pydantic.
    """
    try:
        NetworkScan(network_id=network_id)
        print(f"LOG: Valid IP address format: {network_id}")
        return True
    except ValidationError:
        print(f"LOG: Invalid IP address format: {network_id}")
        return False

@app.get("/scan/{network_id}")
async def scan_network(network_id: str):
    print(f"LOG: Initiating scan for network ID: {network_id}")
    """
    Simulate a network scan for the given network ID.
    """
    if verify_ip_address(network_id):
        print("LOG: Starting network scan...")
        print(f"Scanning network with ID: {network_id}")
        # Simulate scan logic here
        result = scan_ip_for_open_ports(network_id)  # This would be replaced with actual scan logic
        return {"Target": network_id, "Result": result}
    else:
        print("LOG: Scan failed due to invalid IP address format.")
        return {"error": "Invalid IP address format"}
    
@app.get("/scan/{network_id}/portlist/{port_range}")
async def scan_ports(
    network_id: str,
    port_range: str = Path(..., description="Comma-separated list of ports, e.g. '80,443,8080'")
):
    try:
        # Convert port_range string to list of integers
        ports = [int(p) for p in port_range.split(',') if p.strip()]
        
        print(f"LOG: Initiating port scan for network ID: {network_id} with port range: {ports}")
        
        if verify_ip_address(network_id):
            print("LOG: Starting port scan...")
            result = scan_for_port_services(network_id, ports)
            return {"Target": network_id, "Port Range": ports, "Result": result}
        else:
            print("LOG: Port scan failed due to invalid IP address format.")
            return {"error": "Invalid IP address format"}
    except ValueError:
        return {"error": "Invalid port range format. Use comma-separated numbers, e.g. '80,443,8080'"}