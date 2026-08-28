#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoForm Pro Max - Structured Form Dispatch & Submission Logger
Records detailed logs per form for inspection, telemetry, and debugging.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGS_DIR = os.path.join(ROOT_DIR, "data", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

GLOBAL_LOG_FILE = os.path.join(LOGS_DIR, "all_dispatches.jsonl")

def get_form_slug(form_id_or_name: str) -> str:
    s = str(form_id_or_name).lower()
    if "sushi" in s:
        return "sushi_survey"
    elif "seagames" in s or "sea_games" in s:
        return "seagames_survey"
    elif "fda" in s:
        return "fda_expo"
    elif "register" in s or "890" in s or "registration" in s:
        return "registration_890"
    elif "mall" in s:
        return "mall_survey"
    elif "satisfaction" in s:
        return "satisfaction_survey"
    else:
        return "".join(c if c.isalnum() else "_" for c in s).strip("_") or "general_form"

class FormLogger:
    @staticmethod
    def log_submission(
        form_id: str,
        form_name: str,
        engine: str = "HTTPX Async",
        status: str = "SUCCESS", # "SUCCESS" | "RATE_LIMITED" | "FAILED"
        http_code: int = 200,
        latency_ms: int = 250,
        persona: str = "Realistic Respondent",
        details: str = "",
        payload: Optional[Dict[str, Any]] = None,
        batch_index: Optional[int] = None,
        total_batch: Optional[int] = None
    ) -> Dict[str, Any]:
        """บันทึก Log การส่งฟอร์มแต่ละครั้งลงทั้ง JSON Lines และ Human-readable log"""
        now = datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
        timestamp_iso = now.isoformat()
        slug = get_form_slug(form_id or form_name)

        entry_id = f"LOG-{int(time.time() * 1000)}-{slug[:5]}"
        
        log_data = {
            "id": entry_id,
            "timestamp": timestamp_str,
            "timestamp_iso": timestamp_iso,
            "formId": form_id,
            "formSlug": slug,
            "formName": form_name,
            "engine": engine,
            "status": status,
            "httpCode": http_code,
            "latencyMs": latency_ms,
            "persona": persona,
            "details": details or f"Response submitted via {engine} (Status {http_code})",
            "payload": payload or {},
            "batchIndex": batch_index,
            "totalBatch": total_batch
        }

        # 1. Append to Form Specific JSONL
        form_jsonl = os.path.join(LOGS_DIR, f"{slug}.jsonl")
        try:
            with open(form_jsonl, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_data, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[Logger Error] Failed writing {form_jsonl}: {e}")

        # 2. Append to Global JSONL
        try:
            with open(GLOBAL_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_data, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[Logger Error] Failed writing {GLOBAL_LOG_FILE}: {e}")

        # 3. Append to Human Readable .log file
        form_txt_log = os.path.join(LOGS_DIR, f"{slug}.log")
        try:
            with open(form_txt_log, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp_str}] [{status}] [{http_code}] {persona} | {engine} ({latency_ms}ms) | {details}\n")
        except Exception as e:
            pass

        return log_data

    @staticmethod
    def get_logs(form_slug: Optional[str] = None, limit: int = 300, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """ดึงรายการ Logs ย้อนหลังตาม Form หรือทั้งหมด"""
        logs = []
        if form_slug and form_slug != "all":
            resolved_slug = get_form_slug(form_slug)
            target_files = [os.path.join(LOGS_DIR, f"{resolved_slug}.jsonl")]
        else:
            target_files = [os.path.join(LOGS_DIR, f) for f in os.listdir(LOGS_DIR) if f.endswith(".jsonl")]

        for tf in target_files:
            if os.path.exists(tf):
                try:
                    with open(tf, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    entry = json.loads(line)
                                    if status_filter and status_filter != "all":
                                        if entry.get("status") != status_filter and str(entry.get("httpCode")) != status_filter:
                                            continue
                                    logs.append(entry)
                                except Exception:
                                    continue
                except Exception as e:
                    print(f"[Logger Read Error] {tf}: {e}")

        # Sort descending by timestamp / ID
        logs.sort(key=lambda x: x.get("timestamp_iso", x.get("timestamp", "")), reverse=True)
        return logs[:limit]

    @staticmethod
    def get_log_summary() -> Dict[str, Any]:
        """สรุปสถิติ Logs แยกตามแต่ละฟอร์ม"""
        all_logs = FormLogger.get_logs(form_slug="all", limit=5000)
        summary = {
            "totalLogs": len(all_logs),
            "byForm": {},
            "byStatus": {"SUCCESS": 0, "RATE_LIMITED": 0, "FAILED": 0},
            "lastLogTime": all_logs[0]["timestamp"] if all_logs else None
        }

        for item in all_logs:
            f_slug = item.get("formSlug", "unknown")
            if f_slug not in summary["byForm"]:
                summary["byForm"][f_slug] = {
                    "formName": item.get("formName", f_slug),
                    "total": 0,
                    "success": 0,
                    "failed": 0,
                    "lastTimestamp": item.get("timestamp")
                }
            summary["byForm"][f_slug]["total"] += 1
            if item.get("status") == "SUCCESS" or item.get("httpCode") in [200, 302]:
                summary["byForm"][f_slug]["success"] += 1
                summary["byStatus"]["SUCCESS"] += 1
            elif item.get("status") == "RATE_LIMITED" or item.get("httpCode") == 429:
                summary["byForm"][f_slug]["failed"] += 1
                summary["byStatus"]["RATE_LIMITED"] += 1
            else:
                summary["byForm"][f_slug]["failed"] += 1
                summary["byStatus"]["FAILED"] += 1

        return summary
