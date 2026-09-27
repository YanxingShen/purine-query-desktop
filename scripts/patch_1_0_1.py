# -*- coding: utf-8 -*-
"""1.0.1 补丁：修正鹅肉/沙丁鱼/干贝/芦笋，新增带鱼"""
import json, os, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "purine-db.json")

with open(DB, encoding="utf-8") as f:
    db = json.load(f)

items = db["items"]

# 1. 修正鹅肉 C052
for it in items:
    if it["id"] == "C052" and it["name"] == "鹅肉":
        it["purine_mg_per_100g"] = 89
        it["purine_range"] = [89, 140]
        it["level"] = "中"
        it["preparation"] = "烧鹅/可食部"
        it["note"] = "鲜鹅肉因来源而异约89-140；鹅肝(377)另列，勿混淆。指南表1-1把鹅列入75-150第二类"
        if "国家卫健委2024食养指南表1-1" not in it["sources"]:
            it["sources"].append("《成人高尿酸血症与痛风食养指南(2024年版)》表1-1")
        print("Fixed C052 鹅肉")

# 2. 沙丁鱼加注
for it in items:
    if it["name"] == "沙丁鱼":
        it["purine_range"] = [82, 295]
        it["note"] = "食物成分表为82(鲜)，临床常用嘌呤表约295，因测定方法/品种/产地而异；干沙丁鱼/罐头沙丁鱼嘌呤更高，急性期严格避免"
        print("Fixed SH 沙丁鱼")

# 3. 干贝加注
for it in items:
    if it["name"] == "干贝":
        it["purine_range"] = [193, 390]
        it["note"] = "不同来源差异较大(193-390 mg/100g)，干制品嘌呤浓缩，广东省局发布表为390；均属高-极高嘌呤"
        print("Fixed SH 干贝")

# 4. 芦笋：保持 null，清空 range
for it in items:
    if it["name"] == "芦笋":
        it["purine_mg_per_100g"] = None
        it["purine_range"] = []
        it["level"] = "未知"
        it["note"] = "暂无可靠精确数据；鲜芦笋据有限报道约15-25 mg/100g属低嘌呤，植物嘌呤对血尿酸影响小，可正常食用并焯水"
        print("Fixed S 芦笋")

# 5. 新增带鱼（SH 最大编号后接）
sh_nums = [int(it["id"][2:]) for it in items if it["id"].startswith("SH")]
next_sh = max(sh_nums) + 1
new_fish = {
    "id": f"SH{next_sh:03d}",
    "name": "带鱼",
    "aliases": ["刀鱼","裙带鱼","白带鱼"],
    "category": "水产类",
    "subcategory": "鱼类",
    "purine_mg_per_100g": 391.9,
    "purine_range": [290, 392],
    "level": "极高",
    "preparation": "生重/可食部",
    "sources": [
        "《中国食物成分表》第6版（转引自临床常用嘌呤食物表）",
        "《高尿酸血症与痛风患者膳食指导》WS/T 560—2017"
    ],
    "note": "不同来源290-392 mg/100g不等，均属高-极高嘌呤，痛风急性期严格避免；本库原SH060刀鱼(161)为别名重复，已在备注提示以本条为准"
}
# 注意：原 SH060 名为"刀鱼(带鱼)"，与新条目带鱼别名重复。把旧的刀鱼改为说明
for it in items:
    if it["id"] == "SH060":
        it["aliases"] = ["白带鱼(旧录)"]
        it["note"] = "原表记为刀鱼161，与带鱼(SH%03d)为同一物；不同来源差异大，临床通用值约290-392，参见SH%03d" % (next_sh, next_sh)
items.append(new_fish)
print(f"Added new {new_fish['id']} 带鱼")

# 升版本
db["db_version"] = "1.0.1"
db["updated"] = "2026-09-28"

with open(DB, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

# 重新算 sha256
data = open(DB, "rb").read()
sha = hashlib.sha256(data).hexdigest()
print(f"New SHA256: {sha}")
print(f"Item count: {len(items)}")
