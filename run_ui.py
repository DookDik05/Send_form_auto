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
import socket

CANDIDATE_PORTS = [3000, 5000, 8000, 8088, 8888, 5500, 8080]
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Clean logging
        sys.stdout.write(f"[AutoForm UI] {self.address_string()} - {format%args}\n")

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def get_server():
    for port in CANDIDATE_PORTS:
        try:
            server = ReusableTCPServer(("127.0.0.1", port), Handler)
            return server, port
        except (OSError, PermissionError):
            continue
    # Fallback to dynamic port assigned by OS
    server = ReusableTCPServer(("127.0.0.1", 0), Handler)
    return server, server.server_address[1]

def main():
    os.chdir(DIRECTORY)
    httpd, port = get_server()
    url = f"http://127.0.0.1:{port}"
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
    finally:
        httpd.server_close()

if __name__ == "__main__":
    main()

