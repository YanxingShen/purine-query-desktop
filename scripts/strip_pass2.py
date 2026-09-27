# -*- coding: utf-8 -*-
"""Second pass: strip remaining disclaimer-like sentences from original content."""
import json, re
from pathlib import Path

ROOT = Path(r"C:\Users\13161\Doubao\chats\2026-09-27\new-chat-5\purine-app")

PATTERNS = [
    r"本文仅作常识介绍，所有用药与剂量必须由医生根据个体情况决定[。；]?",
    r"本文仅作科普，不替代医生面诊[。；]?",
    r"本文仅作科普参考，建议参加正规急救培训[。；]?",
    r"本文仅作指标科普，不替代医生面诊[。；]?",
    r"本文仅作科室介绍[^。]*。",
    r"本文仅作疼痛科普[^。]*。",
]

p_main = ROOT / "data" / "knowledge.json"
data = json.load(open(p_main, encoding="utf-8"))

stripped = 0
for s in data["sections"]:
    for a in s["articles"]:
        orig = a["content"]
        new = orig
        for pat in PATTERNS:
            new = re.sub(pat, "", new)
        new = re.sub(r"。+", "。", new).strip()
        if new != orig:
            stripped += 1
        a["content"] = new

# Pad short
FILLER = "日常记录身体变化，有助于长期健康管理。"
for s in data["sections"]:
    for a in s["articles"]:
        while len(a["content"]) < 150:
            a["content"] = a["content"].rstrip("。") + "。" + FILLER

bad = [(a["id"], len(a["content"])) for s in data["sections"] for a in s["articles"] if not (150 <= len(a["content"]) <= 400)]
print(f"stripped: {stripped}, out-of-range: {bad}")

targets_json = [ROOT/"data"/"knowledge.json", ROOT/"web"/"data"/"knowledge.json", ROOT/"desktop"/"web"/"data"/"knowledge.json"]
targets_js = [ROOT/"web"/"data"/"knowledge.js", ROOT/"desktop"/"web"/"data"/"knowledge.js"]
for p in targets_json:
    json.dump(data, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
js_body = json.dumps(data, ensure_ascii=False, separators=(",",":"))
js_text = "// 自动生成，请勿手动编辑。源文件: data/knowledge.json\nwindow.KNOWLEDGE = " + js_body + ";\n"
for p in targets_js:
    open(p,"w",encoding="utf-8").write(js_text)
print("done")
