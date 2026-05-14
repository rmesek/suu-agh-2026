from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calculator")

@mcp.tool()
def add(a: float, b: float) -> str:
    """
    Calculator MCP tool

    Add two numbers."""
    return f"{a} + {b} = {a + b}"

@mcp.tool()
def subtract(a: float, b: float) -> str:
    """
    Calculator MCP tool
    Subtract b from a."""
    return f"{a} - {b} = {a - b}"

@mcp.tool()
def multiply(a: float, b: float) -> str:
    """
    Calculator MCP tool
    Multiply two numbers."""
    return f"{a} * {b} = {a * b}"

@mcp.tool()
def divide(a: float, b: float) -> str:
    """
    Calculator MCP tool

    Divide a by b. Refuses division by zero."""
    if b == 0:
        return "Error: division by zero is not allowed."
    return f"{a} / {b} = {a / b}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
