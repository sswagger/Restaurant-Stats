from pydantic import BaseModel
from typing import Optional, Any

class JSONRPCResponse(BaseModel):
    """JSON-RPC 2.0 response."""
    jsonrpc: str = "2.0"
    result: Any = None
    error: Optional[dict] = None
    id: int = 1
