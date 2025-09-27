# src/__main__.py
import asyncio
from .orchestrator import main_flow

if __name__ == "__main__":
    asyncio.run(main_flow())
