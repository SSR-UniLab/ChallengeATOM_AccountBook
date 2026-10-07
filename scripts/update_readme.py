#!/usr/bin/env python3
"""ledger/book.csv の内容を README.md の帳簿表に反映するスクリプト。

Usage:
    python scripts/update_readme.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "ledger" / "book.csv"
README_PATH = ROOT / "README.md"

# README の「現在の帳簿」表に出力する列（CSV のヘッダー名と一致させる）。
# CSV には他に「口座入金 / 口座出金 / 未払金（クレジットカード支払い）」列もあるが、
# 表には従来どおりこの7列のみ出力する。
DISPLAY_COLUMNS = ["購入日", "費目", "内容・購入物", "用途", "金額(税込)", "支払先", "証拠書類の番号"]
AMOUNT_COLUMN = "金額(税込)"
PURPOSE_COLUMN = "用途"

# この列（用途）が空欄の行は帳簿表から除外する。
# 入金・出金（未払金の回収など）の行は用途が空欄になるため、
# 支出ではないこれらの行を除外できる。
FILTER_COLUMN = "用途"

START_MARKER = "<!-- LEDGER:START -->"
END_MARKER = "<!-- LEDGER:END -->"


def load_rows():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = set(DISPLAY_COLUMNS) | {FILTER_COLUMN}
        missing = [c for c in required if c not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(
                "ledger/book.csv に必要な列が見つかりません: " + ", ".join(missing)
            )
        rows = [
            row for row in reader
            if any((value or "").strip() for value in row.values())
        ]

    return rows


def parse_amount(value):
    value = (value or "").strip().replace(",", "")
    return int(value) if value else 0


def format_amount(value):
    if not (value or "").strip():
        return ""
    return f"{parse_amount(value):,}円"


def build_table(rows):
    expense_rows = [
        row for row in rows
        if (row.get(FILTER_COLUMN) or "").strip()
    ]

    aligns = ["---"] * len(DISPLAY_COLUMNS)
    aligns[DISPLAY_COLUMNS.index(AMOUNT_COLUMN)] = "---:"  # 金額列は右寄せ

    lines = [
        "| " + " | ".join(DISPLAY_COLUMNS) + " |",
        "| " + " | ".join(aligns) + " |",
    ]

    total = 0
    for row in expense_rows:
        total += parse_amount(row.get(AMOUNT_COLUMN))
        cells = []
        for col in DISPLAY_COLUMNS:
            if col == AMOUNT_COLUMN:
                cells.append(format_amount(row.get(col)))
            else:
                cells.append((row.get(col) or "").strip())
        lines.append("| " + " | ".join(cells) + " |")

    total_cells = []
    for col in DISPLAY_COLUMNS:
        if col == AMOUNT_COLUMN:
            total_cells.append(f"**{total:,}円**")
        elif col == PURPOSE_COLUMN:
            total_cells.append("**合計**")
        else:
            total_cells.append("")
    lines.append("| " + " | ".join(total_cells) + " |")

    return "\n".join(lines), len(expense_rows)


def update_readme(table):
    text = README_PATH.read_text(encoding="utf-8")
    if START_MARKER not in text or END_MARKER not in text:
        raise SystemExit(
            f"README.md に {START_MARKER} / {END_MARKER} マーカーが見つかりません。"
        )
    before, rest = text.split(START_MARKER, 1)
    _, after = rest.split(END_MARKER, 1)
    new_text = f"{before}{START_MARKER}\n{table}\n{END_MARKER}{after}"
    README_PATH.write_text(new_text, encoding="utf-8")


def main():
    rows = load_rows()
    table, count = build_table(rows)
    update_readme(table)
    print(f"README.md を更新しました。({count}件)")


if __name__ == "__main__":
    main()
