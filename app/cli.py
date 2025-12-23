import argparse
import json
from dataclasses import asdict

from .detector import detect
from .config import PROFILES

def main() -> None:
    parser = argparse.ArgumentParser(prog="pidetect")
    parser.add_argument("path", help="Path to a text file to scan")
    parser.add_argument("--source", default="user", help="user|retrieved_doc|tool_output")
    parser.add_argument("--profile", default="balanced", choices=PROFILES.keys(), help="Detection profile")
    args = parser.parse_args()

    with open(args.path, "r", encoding="utf-8") as f:
        text = f.read()

    result = detect(text, source=args.source, profile=args.profile)
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
