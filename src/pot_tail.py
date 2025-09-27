# src/pot_tail.py
import asyncio
from pathlib import Path

async def tail_potfile(pot_path, on_found):
    pot_path = Path(pot_path)
    pot_path.touch(exist_ok=True)
    with pot_path.open("r", encoding="utf-8", errors="replace") as f:
        f.seek(0, 2)
        while True:
            where = f.tell()
            line = f.readline()
            if not line:
                await asyncio.sleep(1)
                f.seek(where)
                continue
            await on_found(line.strip())
