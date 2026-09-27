#!/usr/bin/env python3
"""为嘌呤数据库中的食物名和别名生成拼音索引，供前端拼音搜索使用。"""
import json
from pypinyin import lazy_pinyin, Style

DB_PATH = r"C:\Users\13161\Doubao\chats\2026-09-27\new-chat-5\purine-app\data\purine-db.json"
OUT_PATH = r"C:\Users\13161\Doubao\chats\2026-09-27\new-chat-5\purine-app\data\pinyin-map.json"


def to_pinyin(text):
    """返回 (全拼空格分隔, 首字母缩写)。非中文字符保留原样。"""
    if not text:
        return "", ""
    # 全拼
    full = " ".join(lazy_pinyin(text, style=Style.NORMAL, errors="default"))
    # 首字母
    initials = "".join(lazy_pinyin(text, style=Style.FIRST_LETTER, errors="default"))
    return full.lower(), initials.lower()


def main():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    pinyin_map = {}
    for item in db["items"]:
        fid = item["id"]
        names = [item["name"]] + item.get("aliases", [])
        entries = []
        for n in names:
            full, init = to_pinyin(n)
            entries.append({"name": n, "full": full, "initials": init})
        pinyin_map[fid] = entries

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(pinyin_map, f, ensure_ascii=False, separators=(",", ":"))

    print(f"已生成拼音索引: {len(pinyin_map)} 条")
    print(f"输出: {OUT_PATH}")
    # 展示几个样例
    for fid in list(pinyin_map.keys())[:3]:
        print(f"  {fid}: {pinyin_map[fid]}")


if __name__ == "__main__":
    main()
