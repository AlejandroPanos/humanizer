#!/usr/bin/env python3
"""Humanize text right from the terminal CLI"""

import argparse
import sys
import os
import anthropic

try:
    import pyperclip

    HAVE_CLIPBOARD = True
except ImportError:
    HAVE_CLIPBOARD = False

SYSTEM_PROMPT = "Void"


def humanize(text: str, model: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
    )
    return response.content[0].text


def main():
    parser = argparse.ArgumentParser(description="Humanize AI generated text")
    parser.add_argument("text", nargs="?", help="Text to humanize (optional)")
    parser.add_argument(
        "-c", "--clipboard", action="store-true", help="Read input from clipboard"
    )
    parser.add_argument(
        "-o", "--copy", action="store-true", help="Copy result to clipboard"
    )
    parser.add_argument("--model", default="claude-sonnet-5")
    args = parser.parse_args()

    if args.clipboard:
        if not HAVE_CLIPBOARD:
            sys.exit("pyperclip not installed.")
        input_text = pyperclip.paste()
    elif args.text:
        input_text = args.text
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()
    else:
        sys.exit(
            "No input provided. Pipe text, pass it as argument, or use --clipboard."
        )

    if not input_text.strip():
        sys.exit("No input")

    result = humanize(input_text, model=args.model)

    if args.copy:
        if not HAVE_CLIPBOARD:
            sys.exit("pyperclip not installed.")
        pyperclip.copy(result)
        print("✅ Copied to clipboard.")

    print(result)


if __name__ == "__main__":
    main()
