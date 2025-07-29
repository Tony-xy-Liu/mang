from pathlib import Path

NAME = Path(__file__).parent.name.lower()
USER = "tony-xy-liu" # github id
GIT_URL = f"https://github.com/{USER}/{NAME}"
SHORT_SUMMARY = "Agent Mang"

_cli_call = "mang.cli:main"
ENTRY_POINTS = [
    f"mang={_cli_call}",
]

with open(Path(__file__).parent/"version.txt") as f:
    VERSION = f.read().strip()

BIND = "localhost:8112"
