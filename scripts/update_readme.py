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

COLUMNS = ["日付", "費目", "内容・購入物", "用途", "金額(税込)", "支払先", "証拠書類の番号"]
CATEGORIES = {"物品費", "交通費", "謝金", "その他"}

START_MARKER = "<!-- LEDGER:START -->"
END_MARKER = "<!-- LEDGER:END -->"


def parse_fields(fields):
    """金額(税込)列にクォートなしのカンマが含まれ、フィールドが余分に
    分割されてしまった場合は、その分を金額列に結合し直す。"""
    n = len(COLUMNS)
    if len(fields) > n:
        extra = len(fields) - n
        amount_idx = COLUMNS.index("金額(税込)")
        merged_amount = ",".join(fields[amount_idx:amount_idx + extra + 1])
        fields = fields[:amount_idx] + [merged_amount] + fields[amount_idx + extra + 1:]
    elif len(fields) < n:
        fields = fields + [""] * (n - len(fields))
    return dict(zip(COLUMNS, fields))


def load_rows():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # ヘッダー行はスキップ
        rows = [parse_fields(fields) for fields in reader if fields]

    for row in rows:
        if row["費目"] not in CATEGORIES:
            print(f"警告: 未定義の費目 '{row['費目']}' (日付: {row['日付']})")

    return rows


def format_amount(value):
    value = value.strip().replace(",", "")
    if not value:
        return ""
    return f"{int(value):,}円"


def build_table(rows):
    aligns = ["---"] * len(COLUMNS)
    aligns[4] = "---:"  # 金額列は右寄せ

    lines = [
        "| " + " | ".join(COLUMNS) + " |",
        "| " + " | ".join(aligns) + " |",
    ]

    total = 0
    for row in rows:
        amount_raw = row["金額(税込)"].strip().replace(",", "")
        total += int(amount_raw) if amount_raw else 0
        cells = [
            row["日付"],
            row["費目"],
            row["内容・購入物"],
            row["用途"],
            format_amount(row["金額(税込)"]),
            row["支払先"],
            row["証拠書類の番号"],
        ]
        lines.append("| " + " | ".join(cells) + " |")

    lines.append(
        "| " + " | ".join(["", "", "", "**合計**", f"**{total:,}円**", "", ""]) + " |"
    )
    return "\n".join(lines)


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
    table = build_table(rows)
    update_readme(table)
    print(f"README.md を更新しました。({len(rows)}件)")


if __name__ == "__main__":
    main()
