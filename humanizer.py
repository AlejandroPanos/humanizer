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
