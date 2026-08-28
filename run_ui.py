#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoForm Pro Max - Frontend Server Launcher
Starts a lightweight local HTTP server and launches the frontend dashboard.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Clean logging
        sys.stdout.write(f"[AutoForm UI] {self.address_string()} - {format%args}\n")

def main():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print("🚀 AutoForm Pro Max - Google Forms Automation Cockpit")
        print(f"📡 Web UI Server running at: {url}")
        print("=" * 60)
        print("Press Ctrl+C to stop the server.")
        
        try:
            webbrowser.open(url)
        except Exception:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down AutoForm UI server.")

if __name__ == "__main__":
    main()
