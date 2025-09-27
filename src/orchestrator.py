# src/orchestrator.py
import asyncio
import os
from pathlib import Path
from .runner import HashcatRunner
from .pot_tail import tail_potfile
from .passgan_stub import passgan_stream

async def on_found(line):
    print("[POTFOUND]", line)

async def on_status(st):
    print("[STATUS]", st["raw"])

async def main_flow():
    workdir = os.getenv("WORKDIR", ".")
    hc = HashcatRunner(hashcat_bin=os.getenv("HASHCAT_BIN","hashcat"), workdir=workdir)
    # small sample args: md5, hashes.txt, wordlist.txt
    args = ["-m", "0", str(Path(workdir)/"sample_hashes/md5.txt"), str(Path(workdir)/"sample_hashes/wordlist.txt")]
    # start pot tail
    pot_task = asyncio.create_task(tail_potfile(Path(workdir)/"hashcat.potfile", on_found))
    rc = await hc.run(args, on_status=on_status, on_found=on_found)
    print("Hashcat returned", rc)
    pot_task.cancel()
