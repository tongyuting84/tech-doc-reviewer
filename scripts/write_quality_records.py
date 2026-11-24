#!/usr/bin/env python3
"""Validate, batch, and write tech-doc review findings to Lark Base."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "质检日期",
    "使用人",
    "文档标题",
    "问题等级",
    "原文描述",
    "问题详情",
}
OPTIONAL_FIELDS = {"文档 URL"}
FORBIDDEN_FIELDS = {"是否修复", "二次质检"}
ALLOWED_LEVELS = {"P0", "P1", "P2"}
BATCH_SIZE = 200


def load_records(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"无法读取有效 JSON：{exc}") from exc

    if not isinstance(payload, dict) or not isinstance(payload.get("create_records"), list):
        raise ValueError('顶层必须是包含 "create_records" 数组的 JSON 对象')

    records = payload["create_records"]
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"第 {index} 条记录不是对象")
        missing = REQUIRED_FIELDS - record.keys()
        if missing:
            raise ValueError(f"第 {index} 条记录缺少字段：{', '.join(sorted(missing))}")
        forbidden = FORBIDDEN_FIELDS & record.keys()
        if forbidden:
            raise ValueError(
                f"第 {index} 条记录包含首次质检禁写字段：{', '.join(sorted(forbidden))}"
            )
        unknown = record.keys() - REQUIRED_FIELDS - OPTIONAL_FIELDS
        if unknown:
            raise ValueError(f"第 {index} 条记录包含未知字段：{', '.join(sorted(unknown))}")
        if record["问题等级"] not in ALLOWED_LEVELS:
            raise ValueError(f"第 {index} 条记录的问题等级必须为 P0、P1 或 P2")
        if not isinstance(record["原文描述"], str) or not record["原文描述"].strip():
            raise ValueError(f"第 {index} 条记录的原文描述不能为空")
        if not isinstance(record["问题详情"], str) or not record["问题详情"].strip():
            raise ValueError(f"第 {index} 条记录的问题详情不能为空")
    return records


def chunks(records: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    return [records[i : i + BATCH_SIZE] for i in range(0, len(records), BATCH_SIZE)]


def write_batch(base_token: str, table_id: str, batch: list[dict[str, Any]]) -> None:
    payload = json.dumps({"create_records": batch}, ensure_ascii=False, separators=(",", ":"))
    command = [
        "lark-cli",
        "base",
        "+record-batch-create",
        "--base-token",
        base_token,
        "--table-id",
        table_id,
        "--json",
        payload,
    ]
    subprocess.run(command, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="校验并批量写入 tech-doc-reviewer 首次质检记录；默认仅校验。"
    )
    parser.add_argument("input", type=Path, help="包含 create_records 的 JSON 文件")
    parser.add_argument("--base-token", help="由 lark-cli 解析得到的真实 Base Token")
    parser.add_argument("--table-id", help="质检记录数据表的真实 table_id")
    parser.add_argument("--apply", action="store_true", help="执行真实写入；不传时只校验")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        records = load_records(args.input)
    except ValueError as exc:
        print(f"校验失败：{exc}", file=sys.stderr)
        return 2

    batches = chunks(records)
    print(f"校验通过：{len(records)} 条记录，{len(batches)} 个批次。")
    if not args.apply:
        print("当前为 dry-run，未写入飞书多维表格。")
        return 0

    if not args.base_token or not args.table_id:
        print("真实写入必须同时提供 --base-token 和 --table-id。", file=sys.stderr)
        return 2

    try:
        for index, batch in enumerate(batches, start=1):
            print(f"正在写入第 {index}/{len(batches)} 批，共 {len(batch)} 条记录。")
            write_batch(args.base_token, args.table_id, batch)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"写入失败：{exc}", file=sys.stderr)
        return 1

    print(f"写入完成：共 {len(records)} 条记录。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
