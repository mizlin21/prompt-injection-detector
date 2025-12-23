import argparse
import json
from dataclasses import asdict

from .detector import detect


def main() -> None:
    parser = argparse.ArgumentParser(prog="pidetect")
    parser.add_argument("path", help="Path to a text file to scan")
    parser.add_argument("--source", default="user", help="user|retrieved_doc|tool_output")
    args = parser.parse_args()

    with open(args.path, "r", encoding="utf-8") as f:
        text = f.read()

    result = detect(text, source=args.source)
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
