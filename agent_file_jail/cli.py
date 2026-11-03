"""Command-line interface for Agent File Jail."""
import argparse
from .jail import FileJail

def main():
    parser = argparse.ArgumentParser(description="Agent File Jail CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate path traversal prevention")
    args = parser.parse_args()

    jail = FileJail(root_dir="/workspace/project")
    test_paths = [
        "src/main.py",
        "../../etc/passwd",
        "certs/server.key",
        "data/nested/report.json"
    ]

    for p in test_paths:
        ok, res = jail.resolve_safe_path(p)
        status = f"SAFE: {res}" if ok else f"BLOCKED: {res}"
        print(f"Path '{p}' -> {status}")

if __name__ == "__main__":
    main()
