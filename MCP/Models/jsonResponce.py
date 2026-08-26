from typing import Optional, Any

class JSONRPCResponse:
    """JSON-RPC 2.0 response."""

    def __init__(self):
        self.jsonrpc: str = "2.0"
        self.result: Any = None
        self.error: Optional[dict] = None
        self.id: int = 1

    def set_result(self, result:str):
        try:
            self.result = result
        except TypeError as ex:
            self.error = {"error": str(ex)}
            return str(ex)

    def to_string(self):
        return {
            "jsonrpc": self.jsonrpc,
            "result": self.result,
            "error": self.error,
            "id": self.id
        }
