# Hashtopolis-Distributive-Dictionary-Attack
An event-driven orchestration framework that automates, monitors, and adaptively schedules Hashcat attacks with optional Hashtopolis integration and AI candidate generation.


How to set this up in WSL (step-by-step)

Open WSL (Ubuntu or your distro).

Install prerequisites:

sudo apt update
sudo apt install -y git python3 python3-venv python3-pip build-essential
# Install hashcat
sudo apt install -y hashcat


(GPU in WSL2) If you want GPU acceleration, follow NVIDIA's WSL docs — install NVIDIA WSL drivers on Windows and the CUDA toolkit in WSL. If not set up, hashcat will run CPU-only or fail for GPU modes.

Clone your repo:

git clone git@github.com:youruser/adaptive-hashcat-orch.git
cd adaptive-hashcat-orch
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt   # or pip install aiohttp requests python-dotenv watchdog


Copy .env.example to .env and fill in values.

Run a test (simple)

Create sample_hashes/md5.txt with a single md5 hash (e.g. 5f4dcc3b5aa765d61d8327deb882cf99 which is password).

Create sample_hashes/wordlist.txt with password on one line.

From repo root:

source .venv/bin/activate
python -m src


You should see Hashcat startup lines and the FOUND or potfile being tailed.

Edit on the fly (hot reload)

Use VS Code Remote-WSL: open WSL shell, code . → it opens the project in VS Code connected to WSL. Edits are immediate.

To auto-restart the Python process when you edit code, use watchdog's watchmedo:

pip install watchdog
# from repo root
watchmedo auto-restart --patterns="*.py" --recursive -- python -m src


Now when you edit a .py file and save, it restarts the process automatically — great for iterative dev.

Alternative: run inside the VS Code debugger with an auto-reload extension or use entr:

ls src/*.py | entr -r python -m src

Making it compatible with Hashtopolis

Put your Hashtopolis URL & API key into .env.

Implement the HashtopolisClient functions you need (task creation, upload wordlists, fetch results). Hashtopolis uses a JSON API — usually /api/tasks/create etc. (Check your Hashtopolis server docs; I can generate the exact client functions if you paste your Hashtopolis API docs or sample endpoints.)

Wire HashtopolisClient.create_task(...) inside orchestrator.py to create tasks or to notify the server when something is found.

Is the code I gave functional?

The code I wrote above is a working skeleton: it will launch hashcat (if installed), tail a potfile, and print status/found lines.

It’s intentionally minimal so you can test quickly and extend safely.

Production hardening steps you should add:

Robust parsing of --machine-readable lines to extract speed/progress.

Logging with logging module, not print.

Retry and watchdog for stuck Hashcat processes.

Persisting results to SQLite for auditing.

Proper Hashtopolis API client with error handling and authentication.

Development tools I recommend

VS Code + Remote - WSL — best for editing in WSL and debugging.

GitHub, obviously — create a repo, push branch, use PRs.

GitHub Copilot or Cursor — AI pair programming to speed up writing clients/parsers.

Use pre-commit (black, flake8) for consistent style.

GPU / WSL notes (important)

WSL2: requires NVIDIA driver for WSL on Windows host + CUDA toolkit in WSL. See NVIDIA docs. Without it, hashcat will default to CPU.

If you plan to use remote Vast.ai GPUs, you’ll likely run agents there (Hashtopolis agents) — your orchestration code can still run in a coordinator role and talk to Hashtopolis via API.

Next steps I can do for you right now (pick one)

Generate a complete ready-to-copy GitHub repo zip (full files above, plus README and CI) you can paste into your repo.

Implement a full HashtopolisClient for your server (I’ll need the API base path or doc — you already gave some of this in past chats).

Add advanced machine-readable Hashcat parsing and an attack scheduler based on metrics (progress, speed, restore points).

Walk you through installing GPU drivers for WSL2 if you want GPU acceleration.

Tell me which option you want and I’ll produce the files or the specific client code next — no waiting.
