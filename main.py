from fastapi import FastAPI
from pydantic import BaseModel, IPvAnyAddress, ValidationError
from typing import Union

app = FastAPI(title="Agentic Network Mapper", version="0.1.0")

class NetworkScan(BaseModel):
    network_id: Union[IPvAnyAddress, str]

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
        return {"network_id": network_id, "status": "Scan completed"}
    else:
        print("LOG: Scan failed due to invalid IP address format.")
        return {"error": "Invalid IP address format"}