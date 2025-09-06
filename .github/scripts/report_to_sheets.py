#!/usr/bin/env python
import argparse, csv, json, os, sys, datetime
import gspread
from google.oauth2.service_account import Credentials

ASSIGNMENT_COLUMNS = [
    "github_username",
    "total_score",
    "overridden_score",
    "dont_mark_late",
    "commit_sha",
    "timestamp_utc",
]

def get_total_from_csv(csv_path: str) -> float:
    if not os.path.exists(csv_path):
        return 0.0
    total = 0.0
    total_row = None
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        for r in rows:
            if r.get("test_id", "").strip().upper() == "TOTAL":
                total_row = r
                break
    if not total_row:
        # Fallback: sum points_awarded
        total = sum(float(r.get("points_awarded", 0) or 0) for r in rows)
        return round(total, 2)
    return float(total_row.get("points_awarded", 0) or 0)

def ensure_tab(gc, sheet_id: str, tab_name: str):
    sh = gc.open_by_key(sheet_id)
    try:
        ws = sh.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=tab_name, rows=1000, cols=len(ASSIGNMENT_COLUMNS))
        ws.append_row(ASSIGNMENT_COLUMNS)
    else:
        # Ensure header exists & matches (lightweight)
        hdr = ws.row_values(1)
        if [h.strip() for h in hdr] != ASSIGNMENT_COLUMNS:
            # Optionally: rewrite header (non-destructive if columns differ)
            ws.update("A1", [ASSIGNMENT_COLUMNS])
    return ws

def upsert_row(ws, username: str, total_score: float, commit_sha: str):
    # Find username in column A
    usernames = ws.col_values(1)  # includes header
    try:
        idx = [u.strip() for u in usernames].index(username, 1)  # start after header
        row_num = idx + 1
    except ValueError:
        # Append new row with defaults
        now = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
        ws.append_row([
            username,                # github_username
            round(total_score, 2),   # total_score
            "",                      # overridden_score
            "FALSE",                 # dont_mark_late
            commit_sha,              # commit_sha
            now,                     # timestamp_utc
        ])
        return

    # Update existing row: keep overridden_score and dont_mark_late as-is; refresh total/commit/timestamp
    row = ws.row_values(row_num)
    # Pad row to required length
    row = (row + [""] * len(ASSIGNMENT_COLUMNS))[:len(ASSIGNMENT_COLUMNS)]
    row[0] = username
    row[1] = str(round(total_score, 2))
    # row[2] = overridden_score (leave as-is)
    # row[3] = dont_mark_late (leave as-is)
    row[4] = commit_sha
    row[5] = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    ws.update(f"A{row_num}:F{row_num}", [row])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet-id", required=True)
    ap.add_argument("--tab", required=True)
    ap.add_argument("--username", required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--scores-csv", default="test_scores.csv")
    args = ap.parse_args()

    creds_json = os.environ.get("SHEETS_SERVICE_ACCOUNT_JSON")
    if not creds_json:
        print("Missing SHEETS_SERVICE_ACCOUNT_JSON", file=sys.stderr)
        sys.exit(1)
    info = json.loads(creds_json)
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    gc = gspread.authorize(creds)

    total = get_total_from_csv(args.scores_csv)
    ws = ensure_tab(gc, args.sheet_id, args.tab)
    upsert_row(ws, args.username, total, args.commit)

if __name__ == "__main__":
    main()
