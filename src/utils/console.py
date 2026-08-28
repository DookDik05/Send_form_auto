#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoForm Utils - Console Formatter & Cross-Platform UTF-8 Helper
"""

import sys

def setup_utf8_console():
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

def print_banner(title: str, subtitle: str = ""):
    setup_utf8_console()
    width = 75
    print("=" * width)
    print(f"🚀 {title}")
    if subtitle:
        print(f"   {subtitle}")
    print("=" * width)

def print_summary_card(metrics: dict):
    setup_utf8_console()
    print("\n" + "-" * 60)
    print("🏁 EXECUTION SUMMARY")
    for k, v in metrics.items():
        print(f"  • {k}: {v}")
    print("-" * 60 + "\n")
