# src/runner.py
import asyncio
from pathlib import Path
import shlex
import os

class HashcatRunner:
    def __init__(self, hashcat_bin="hashcat", workdir=".", potfile="hashcat.potfile"):
        self.hashcat_bin = hashcat_bin
        self.workdir = Path(workdir)
        self.potfile = self.workdir / potfile
        self.proc = None

    async def run(self, args, on_status=None, on_found=None):
        cmd = [self.hashcat_bin, "--status", "--status-timer=5", "--machine-readable", "--potfile-path", str(self.potfile)] + args
        self.proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(self.workdir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        print("Started:", " ".join(shlex.quote(x) for x in cmd))
        while True:
            raw = await self.proc.stdout.readline()
            if not raw:
                if self.proc.returncode is None:
                    await asyncio.sleep(0.1)
                    continue
                break
            line = raw.decode(errors="replace").strip()
            if not line:
                continue
            # quick machine-readable parsing
            if line.startswith("STATUS"):
                if on_status:
                    await on_status({"raw": line})
            elif line.startswith("FOUND"):
                if on_found:
                    await on_found(line.split("\t",1)[1] if "\t" in line else line)
            else:
                # other hashcat output, useful for debugging
                print("[HC]", line)
        rc = await self.proc.wait()
        return rc

    async def feed_stdin(self, candidates):
        if self.proc and self.proc.stdin:
            for cand in candidates:
                self.proc.stdin.write(cand.encode() + b"\n")
            await self.proc.stdin.drain()
