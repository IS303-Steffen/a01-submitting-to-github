#!/usr/bin/env python
import argparse
import csv
import json
import os
import sys
import datetime
import re
import time
from zoneinfo import ZoneInfo

import gspread
from google.oauth2.service_account import Credentials

ASSIGNMENT_COLUMNS = [
    "github_username",
    "total_score",
    "overridden_score",
    "dont_mark_late",
    "commit_sha",
    "timestamp",
]


# -------------------------------
# Helpers
# -------------------------------

def canonical_tab_name(name: str) -> str:
    """Canonicalize a worksheet title: lowercase, underscores, alnum only, ≤100 chars."""
    s = (name or "").strip().lower()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^a-z0-9_]", "_", s)
    return s[:100]  # Sheets limit


def _col_letter(n: int) -> str:
    """Convert 1-based column index to A1 notation letter(s)."""
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _get_ws_case_insensitive(sh, desired: str):
    """Try exact match first, then case-insensitive match."""
    for ws in sh.worksheets():
        if ws.title == desired:
            return ws
    desired_ci = desired.casefold()
    for ws in sh.worksheets():
        if ws.title.casefold() == desired_ci:
            return ws
    return None


def ensure_tab(gc, sheet_id: str, tab_name: str):
    """Idempotently get/create a worksheet named `tab_name` (canonicalized) and ensure header row."""
    tab_name = canonical_tab_name(tab_name)
    if not tab_name:
        raise ValueError("ASSIGNMENT_TAB is empty after canonicalization.")

    sh = gc.open_by_key(sheet_id)

    ws = _get_ws_case_insensitive(sh, tab_name)
    if ws is None:
        # Not found, create it
        try:
            ws = sh.add_worksheet(title=tab_name, rows=1000, cols=len(ASSIGNMENT_COLUMNS))
        except gspread.exceptions.APIError as e:
            # If creation failed because it already exists (race), retry fetch
            msg = str(e).lower()
            try:
                err_json = e.response.json()
                msg = err_json.get("error", {}).get("message", msg).lower()
            except Exception:
                pass
            if "already exists" in msg:
                ws = _get_ws_case_insensitive(sh, tab_name)
            else:
                raise
        # retry fetch to handle eventual consistency
        for _ in range(5):
            if ws:
                break
            time.sleep(0.3)
            ws = _get_ws_case_insensitive(sh, tab_name)
        if not ws:
            raise gspread.exceptions.WorksheetNotFound(f"{tab_name} (created but not visible after retries)")
    else:
        # If found but case differs, normalize title
        if ws.title != tab_name:
            try:
                ws.update_title(tab_name)
            except Exception:
                # Not fatal, but keep going with existing
                pass

    # Ensure header row matches exactly
    try:
        first_row = ws.row_values(1)
    except Exception:
        first_row = []
    if [c.strip() for c in first_row] != ASSIGNMENT_COLUMNS:
        end_col = _col_letter(len(ASSIGNMENT_COLUMNS))
        ws.update(f"A1:{end_col}1", [ASSIGNMENT_COLUMNS])

    return ws


def get_total_from_csv(csv_path: str) -> float:
    if not os.path.exists(csv_path):
        return 0.0
    total_row = None
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("test_id", "").strip().upper() == "TOTAL":
                total_row = r
                break
    if not total_row:
        return 0.0
    return float(total_row.get("points_awarded", 0) or 0)


def upsert_row(ws, username: str, total_score: float, commit_sha: str):
    usernames = ws.col_values(1)  # includes header
    try:
        idx = [u.strip() for u in usernames].index(username, 1)  # skip header
        row_num = idx + 1
    except ValueError:
        # Append new
        now = datetime.datetime.now(ZoneInfo("America/Denver")).isoformat(timespec="seconds")
        ws.append_row([
            username,
            round(total_score, 2),
            "",
            "FALSE",
            commit_sha,
            now,
        ])
        return

    # Update existing row (preserve overridden_score and dont_mark_late)
    row = ws.row_values(row_num)
    row = (row + [""] * len(ASSIGNMENT_COLUMNS))[:len(ASSIGNMENT_COLUMNS)]
    row[0] = username
    row[1] = str(round(total_score, 2))
    # row[2] overridden_score untouched
    # row[3] dont_mark_late untouched
    row[4] = commit_sha
    row[5] = datetime.datetime.now(ZoneInfo("America/Denver")).isoformat(timespec="seconds")
    ws.update(f"A{row_num}:{_col_letter(len(ASSIGNMENT_COLUMNS))}{row_num}", [row])


# -------------------------------
# Main
# -------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet-id", required=True)
    ap.add_argument("--tab", required=True)
    ap.add_argument("--username", required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--scores-csv", default="tests/test_scores.csv")
    args = ap.parse_args()

    creds_json = os.environ.get("SHEETS_SERVICE_ACCOUNT_JSON")
    if not creds_json:
        print("Missing SHEETS_SERVICE_ACCOUNT_JSON", file=sys.stderr)
        sys.exit(1)
    info = json.loads(creds_json)
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    gc = gspread.authorize(creds)

    tab = canonical_tab_name(args.tab)
    total = get_total_from_csv(args.scores_csv)
    ws = ensure_tab(gc, args.sheet_id, tab)
    upsert_row(ws, args.username, total, args.commit)


if __name__ == "__main__":
    main()