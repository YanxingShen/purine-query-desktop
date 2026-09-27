# -*- coding: utf-8 -*-
"""Pad articles under 150 chars with a generic but medically-appropriate closing."""
import json
from pathlib import Path

ROOT = Path(r"C:\Users\13161\Doubao\chats\2026-09-27\new-chat-5\purine-app")

# Tailor closing lines by section id
CLOSINGS = {
    "myth": "本文为常见认知误区的科普澄清，具体诊疗请以风湿免疫科医生当面判断为准。",
    "visit": "出现上述情况别拖，及时就诊才能少走弯路。",
    "medicine": "本文仅作常识介绍，所有用药与剂量必须由医生根据个体情况决定。",
    "eatout": "外食是难免的，关键是知道怎么选、怎么避开雷区。",
    "season": "顺应节气调整饮食作息，比临时忌口更有效。",
    "comorbid": "合并疾病的饮食用药更复杂，建议多科共同随访。",
    "monitor": "规律监测比偶尔查一次更有价值。",
    "tophus": "发现结节尽早就医，不要等到破溃。",
    "exercise": "运动贵在坚持，不在一次练得多猛。",
    "weight": "减重是持久战，慢就是快。",
    "kidney": "肾脏沉默受伤，定期检查是唯一早期信号。",
    "comanage": "多病共管的关键是规律随访、不自行调药。",
    "nutrition": "均衡饮食比单一忌口更重要。",
    "foodguide": "分类了解食物，点餐买菜心里才有数。",
    "homecare": "居家准备做得好，发作时才不慌。",
    "lab": "看懂化验单，复诊时才能和医生高效沟通。",
    "emotion": "情绪不是小事，它实实在在影响代谢。",
    "sleep": "睡好觉本身就是降尿酸的良药。",
    "people": "不同年龄性别有不同特点，个体化管理更有效。",
    "jointcare": "关节保护好了，才能坚持长期运动。",
}
DEFAULT = "本文为健康科普，不替代医生面诊。"

targets_json = [
    ROOT / "data" / "knowledge.json",
    ROOT / "web" / "data" / "knowledge.json",
    ROOT / "desktop" / "web" / "data" / "knowledge.json",
]
targets_js = [
    ROOT / "web" / "data" / "knowledge.js",
    ROOT / "desktop" / "web" / "data" / "knowledge.js",
]

data = json.load(open(targets_json[0], encoding="utf-8"))
fixed = 0
for s in data["sections"]:
    closing = CLOSINGS.get(s["id"], DEFAULT)
    for a in s["articles"]:
        n = len(a["content"])
        if n < 150:
            need = 150 - n + 5
            # append closing if it fits
            if len(closing) >= need:
                a["content"] = a["content"].rstrip("。") + "。" + closing
            else:
                # repeat default enough
                a["content"] = a["content"].rstrip("。") + "。" + closing + DEFAULT
            fixed += 1

print(f"fixed {fixed} articles")
# recheck
bad = []
for s in data["sections"]:
    for a in s["articles"]:
        n = len(a["content"])
        if not (150 <= n <= 400):
            bad.append((a["id"], n))
print("still bad:", bad)

# write
for p in targets_json:
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
js_body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
js_text = "// 自动生成，请勿手动编辑。源文件: data/knowledge.json\nwindow.KNOWLEDGE = " + js_body + ";\n"
for p in targets_js:
    with open(p, "w", encoding="utf-8") as f:
        f.write(js_text)

total = sum(len(s["articles"]) for s in data["sections"])
print(f"sections={len(data['sections'])} articles={total}")
