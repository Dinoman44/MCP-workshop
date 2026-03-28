import httpx
from typing import Tuple
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("FastMCP Example")

@mcp.tool()
async def count_letters_in_word(word: str, letter: str) -> int:
    """Counts the number of times a letter appears in a word."""
    return word.count(letter)

@mcp.tool()
async def solve_quadratic(a: float, b: float, c: float) -> Tuple[float, float]:
    """Solves the quadratic equation ax^2 + bx + c = 0 and returns the roots."""
    d = b**2 - 4*a*c
    if d < 0:
        raise ValueError("No real roots")
    root1 = (-b + d**0.5) / (2*a)
    root2 = (-b - d**0.5) / (2*a)
    return root1, root2

@mcp.tool()
async def query_nusmods_course(course: str) -> dict:
    """Queries the NUSMods API for course information."""
    url = f"https://api.nusmods.com/v2/2025-2026/modules/{course}.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")