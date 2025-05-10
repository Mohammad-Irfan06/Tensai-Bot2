import asyncio
from handler.start import start_bot

async def main():
    start_bot()
    await asyncio.sleep(5)  # Simulate bot running
    
if __name__ == "__main__":
    asyncio.run(main())
