import argparse
import json
from dataclasses import asdict

from .detector import detect
from .config import PROFILES
from .rag_scanner import rag_scan

def scan_file(path: str, source: str, profile: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    result = detect(text, source=source, profile=profile)
    print(json.dumps(asdict(result), indent=2))

def scan_rag_bundle(path: str, profile: str, chunk_size: int, overlap: int) -> None:
    with open(path, "r", encoding="utf-8") as f:
        docs = json.load(f)
    result = rag_scan(docs, profile=profile, chunk_size=chunk_size, overlap=overlap)
    print(json.dumps(asdict(result), indent=2))

def main() -> None:
    parser = argparse.ArgumentParser(prog="pidetect")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Single-file scan
    p_scan = sub.add_parser("scan", help="Scan a single text file")
    p_scan.add_argument("path", help="Path to a text file to scan")
    p_scan.add_argument("--source", default="user", help="user|retrieved_doc|tool_output")
    p_scan.add_argument("--profile", default="balanced", choices=PROFILES.keys(), help="Detection profile")

    # RAG scan
    p_rag = sub.add_parser("rag", help="Scan a JSON bundle of retrieved documents")
    p_rag.add_argument("path", help="Path to JSON list of docs (doc_id, source, text)")
    p_rag.add_argument("--profile", default="strict", choices=PROFILES.keys(), help="Detection profile")
    p_rag.add_argument("--chunk-size", type=int, default=400)
    p_rag.add_argument("--overlap", type=int, default=80)

    args = parser.parse_args()

    if args.cmd == "scan":
        scan_file(args.path, source=args.source, profile=args.profile)
    elif args.cmd == "rag":
        scan_rag_bundle(args.path, profile=args.profile, chunk_size=args.chunk_size, overlap=args.overlap)


if __name__ == "__main__":
    main()


