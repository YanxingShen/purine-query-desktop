# -*- coding: utf-8 -*-
"""
purine-db.json 校验脚本
输出：总条目数、各大类条目数、等级分布、重复 id/重复名称检查、缺 source 检查、等级与数值匹配检查
"""
import json, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "purine-db.json")

def expected_level(v):
    if v is None:
        return "未知"
    if v < 75:
        return "低"
    if v < 150:
        return "中"
    if v <= 300:
        return "高"
    return "极高"

def main():
    with open(DB, encoding="utf-8") as f:
        db = json.load(f)
    items = db["items"]
    print("=" * 60)
    print(f"数据库版本: {db['db_version']}  更新日期: {db['updated']}")
    print(f"总条目数: {len(items)}")
    print("=" * 60)

    # 各大类条目数
    cat = Counter(it["category"] for it in items)
    print("\n【各大类条目数】")
    for c in db["categories"]:
        print(f"  {c:8s}: {cat.get(c,0):3d} 条")
    missing_cats = [c for c in db["categories"] if cat.get(c,0)==0]
    if missing_cats:
        print(f"  !! 缺失大类: {missing_cats}")

    # 等级分布
    lvl = Counter(it["level"] for it in items)
    print("\n【等级分布】")
    for k in ["低","中","高","极高","未知"]:
        print(f"  {k:4s}: {lvl.get(k,0):3d} 条")

    # 重复 id
    ids = [it["id"] for it in items]
    dup_ids = [k for k,v in Counter(ids).items() if v>1]
    print(f"\n【重复 id 检查】: {'发现重复: '+str(dup_ids) if dup_ids else 'OK 无重复'}")

    # 重复名称
    names = [it["name"] for it in items]
    dup_names = [k for k,v in Counter(names).items() if v>1]
    print(f"【重复名称检查】: {'发现重复: '+str(dup_names) if dup_names else 'OK 无重复'}")

    # 缺 source
    no_src = [it["id"]+":"+it["name"] for it in items if not it.get("sources") or len(it["sources"])==0]
    print(f"【缺 source 检查】: {'发现缺source: '+str(no_src) if no_src else 'OK 每条均有来源'}")

    # 等级与数值匹配
    mismatch = []
    for it in items:
        exp = expected_level(it["purine_mg_per_100g"])
        if exp != it["level"]:
            mismatch.append(f"{it['id']} {it['name']} value={it['purine_mg_per_100g']} level={it['level']} expected={exp}")
    print(f"【等级与数值匹配检查】: {'发现错配:\n    '+'\n    '.join(mismatch) if mismatch else 'OK 全部匹配'}")

    # range 检查
    bad_range = []
    for it in items:
        v = it["purine_mg_per_100g"]
        r = it.get("purine_range")
        if v is not None:
            if r is None:
                bad_range.append(f"{it['id']} range missing")
            elif not (r[0] <= v <= r[1]):
                bad_range.append(f"{it['id']} range {r} not contain {v}")
    print(f"【purine_range 一致性检查】: {'问题: '+str(bad_range) if bad_range else 'OK'}")

    print("\n" + "=" * 60)
    print("校验完成")

if __name__ == "__main__":
    main()
