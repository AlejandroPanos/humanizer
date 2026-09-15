#!/usr/bin/env python3
"""Humanize text right from the terminal CLI"""

import argparse
import sys
import anthropic

try:
    import pyperclip

    HAVE_CLIPBOARD = True
except ImportError:
    HAVE_CLIPBOARD = False
