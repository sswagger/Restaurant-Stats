from pydantic import BaseModel

class JSONRPCRequest(BaseModel):
    """JSON-RPC 2.0 request."""
    jsonrpc: str = "2.0"
    method: str
    params: dict = {}
    id: int = 1
