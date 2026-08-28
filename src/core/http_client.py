#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoForm Core - HTTP Async Engine & Browser Signature Rotation
"""

import re
import random
import httpx

CLIENT_PROFILES = [
    {
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "ch_ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "ch_mobile": "?0",
        "ch_platform": '"Windows"'
    },
    {
        "ua": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "ch_ua": '"Chromium";v="123", "Google Chrome";v="123", "Not-A.Brand";v="99"',
        "ch_mobile": "?0",
        "ch_platform": '"Windows"'
    },
    {
        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "ch_ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "ch_mobile": "?0",
        "ch_platform": '"macOS"'
    },
    {
        "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
        "ch_ua": None,
        "ch_mobile": "?1",
        "ch_platform": '"iOS"'
    },
    {
        "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36",
        "ch_ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "ch_mobile": "?1",
        "ch_platform": '"Android"'
    }
]

def get_random_browser_profile():
    return random.choice(CLIENT_PROFILES)

def build_browser_headers(profile: dict, referer_url: str):
    headers = {
        "User-Agent": profile["ua"],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": referer_url,
        "Origin": "https://docs.google.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    if profile.get("ch_ua"):
        headers["Sec-Ch-Ua"] = profile["ch_ua"]
        headers["Sec-Ch-Ua-Mobile"] = profile["ch_mobile"]
        headers["Sec-Ch-Ua-Platform"] = profile["ch_platform"]
    return headers

async def fetch_form_security_tokens(client: httpx.AsyncClient, view_url: str, headers: dict, timeout: float = 20.0):
    """
    Performs handshake GET to acquire live fbzx token and page state.
    """
    view_headers = {
        **headers,
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        resp = await client.get(view_url, headers=view_headers, timeout=timeout)
        html = resp.text
        
        def grab(pat, default=""):
            m = re.search(pat, html)
            return m.group(1) if m else default

        return {
            "fbzx": grab(r'name="fbzx"\s+value="([^"]+)"', "-969805304991096499"),
            "fvv": grab(r'name="fvv"\s+value="([^"]+)"', "1"),
            "pageHistory": grab(r'name="pageHistory"\s+value="([^"]+)"', "0,1")
        }
    except Exception:
        return {"fbzx": "-969805304991096499", "fvv": "1", "pageHistory": "0,1"}
