from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Example MCP Server")

@mcp.tool()
async def count_letters_in_word(letter: str, word: str) -> int:
    """Count the number of occurrences of a letter in a word."""
    return word.count(letter)

if __name__ == "__main__":
    mcp.run(transport="stdio")