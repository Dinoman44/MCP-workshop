import asyncio
from fast_agent.core.fastagent import FastAgent

fast = FastAgent("Agent Example")

@fast.agent(
    instruction="Given an object, respond only with an estimate of its size."
)
async def main():
    async with fast.run() as agent:
        await agent()

if __name__ == "__main__":
    asyncio.run(main())