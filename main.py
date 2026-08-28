#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoForm Pro Max - Unified Command Line Interface
The central CLI entrypoint for running form automations, inspecting forms, and launching web dashboard.
"""

import argparse
import asyncio
import sys

from src.utils.console import setup_utf8_console, print_banner
from src.utils.csv_manager import scan_all_csv_history
from src.runners.sushi_runner import run_sushi_async, run_sushi_selenium

def cmd_list(args):
    setup_utf8_console()
    print_banner("AutoForm Pro Max - Registered Form Campaigns")
    categories = scan_all_csv_history()
    print(f"{'Form Name':<42} | {'Form ID':<22} | {'Submissions':<12} | {'Runs'}")
    print("-" * 88)
    for c in categories:
        print(f"{c['icon']} {c['name']:<38} | {c['formId'][:18] + '...':<22} | {c['totalSent']:<12} | {c['runsCount']} batches")
    print("-" * 88)

def cmd_run(args):
    form_target = args.target.lower()
    if form_target in ("sushi", "sushi_survey"):
        asyncio.run(run_sushi_async(count=args.count, concurrency=args.concurrency, mode=args.mode))
    else:
        print(f"Unknown target: '{args.target}'. Available targets: sushi")

def cmd_selenium(args):
    form_target = args.target.lower()
    if form_target in ("sushi", "sushi_survey"):
        run_sushi_selenium(count=args.count, headless=not args.visual)
    else:
        print(f"Unknown target: '{args.target}'. Available targets: sushi")

def cmd_ui(args):
    import subprocess
    print_banner("AutoForm Pro Max - Launching Web Dashboard")
    subprocess.run([sys.executable, "run_ui.py"])

def cmd_stats(args):
    setup_utf8_console()
    categories = scan_all_csv_history()
    total_all = sum(c['totalSent'] for c in categories)
    print_banner("AutoForm Pro Max - Real Disk Telemetry Stats", f"Total Submissions: {total_all:,}")
    for c in categories:
        print(f"• {c['icon']} {c['name']}: {c['totalSent']:,} submissions ({c['runsCount']} files)")
    print("")

def main():
    setup_utf8_console()
    parser = argparse.ArgumentParser(
        description="AutoForm Pro Max - Google Forms Automation Cockpit",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: list
    subparsers.add_parser("list", help="List all configured form campaigns")

    # Command: stats
    subparsers.add_parser("stats", help="Display submission statistics scanned from disk")

    # Command: ui
    subparsers.add_parser("ui", help="Start web dashboard cockpit")

    # Command: run (Async HTTPX)
    p_run = subparsers.add_parser("run", help="Run form automation using async HTTPX engine")
    p_run.add_argument("target", choices=["sushi"], help="Form target to execute")
    p_run.add_argument("--count", "-n", type=int, default=50, help="Number of submissions")
    p_run.add_argument("--concurrency", "-c", type=int, default=5, help="Worker coroutines")
    p_run.add_argument("--mode", "-m", choices=["fast", "human", "stealth"], default="human", help="Pacing & delay profile")

    # Command: selenium (Visual / Headless Browser)
    p_sel = subparsers.add_parser("selenium", help="Run form automation using Selenium browser")
    p_sel.add_argument("target", choices=["sushi"], help="Form target to execute")
    p_sel.add_argument("--count", "-n", type=int, default=5, help="Number of responses")
    p_sel.add_argument("--visual", action="store_true", help="Show real Chrome browser window")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "selenium":
        cmd_selenium(args)
    elif args.command == "ui":
        cmd_ui(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
