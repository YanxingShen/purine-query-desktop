# -*- coding: utf-8 -*-
"""Strip repeated disclaimer sentences from article content.
Keep sources and top-level disclaimer intact."""
import json
import re
from pathlib import Path

ROOT = Path(r"C:\Users\13161\Doubao\chats\2026-09-27\new-chat-5\purine-app")

# Phrases to strip (whole sentences ending with 。)
DISCLAIMER_PATTERNS = [
    r"本文为健康科普，不替代医生面诊[。；]?",
    r"本文为健康科普，不替代医生面诊；情况危急请立即拨打120[。；]?",
    r"本文仅作科室介绍，具体挂号和诊疗请以医院分诊台和医生判断为准[。；]?",
    r"本文仅作疼痛科普，不能替代医生面诊；?出现剧烈、持续、新发的疼痛，建议及时就诊[。；]?",
    r"本文仅作疼痛科普，不能替代医生面诊[。；]?",
    r"本文仅作科普参考，强烈建议参加红十字会等正规急救培训并考取证书，光看文字不能真正救人[。；]?",
    r"本文仅作科普，不替代医生诊断[。；]?",
    r"器官保护是长期功课，定期体检和良好生活方式是基础[。；]?",
    r"急救仅为临时处理，事后仍需就医评估；情况危急请立即拨打120[。；]?",
    r"急救仅为临时处理，事后仍需就医评估[。；]?",
    r"老年人体感不敏感，有不适及早就医，不要拖[。；]?",
    r"特殊人群用药和饮食需个体化，务必在医生指导下进行[。；]?",
    r"症状只是信号，原因需医生结合检查判断，不要自行对号入座[。；]?",
    r"本文不涉及具体药物和剂量，一切用药请遵医嘱[。；]?",
    r"本文为健康科普，不替代医生面诊；?情况危急请立即拨打120[。；]?",
    r"本文仅作指标科普，不替代医生面诊[。；]?",
    r"本文仅作疼痛科普，不替代医生面诊；?出现剧烈、持续、新发的疼痛建议及时就诊[。；]?",
]

p_main = ROOT / "data" / "knowledge.json"
data = json.load(open(p_main, encoding="utf-8"))

stripped_count = 0
still_short = []

for s in data["sections"]:
    for a in s["articles"]:
        orig = a["content"]
        new = orig
        for pat in DISCLAIMER_PATTERNS:
            new = re.sub(pat, "", new)
        # cleanup double punctuation / spaces
        new = re.sub(r"。+", "。", new)
        new = re.sub(r"^。+", "", new).strip()
        if new != orig:
            stripped_count += 1
        a["content"] = new
        if len(new) < 150:
            still_short.append((a["id"], len(new)))

print(f"stripped in {stripped_count} articles")
print(f"still <150 chars: {len(still_short)}")
for aid, n in still_short[:80]:
    print(f"  {aid}: {n}")

# Write
targets_json = [
    ROOT / "data" / "knowledge.json",
    ROOT / "web" / "data" / "knowledge.json",
    ROOT / "desktop" / "web" / "data" / "knowledge.json",
]
targets_js = [
    ROOT / "web" / "data" / "knowledge.js",
    ROOT / "desktop" / "web" / "data" / "knowledge.js",
]
for p in targets_json:
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
js_body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
js_text = "// 自动生成，请勿手动编辑。源文件: data/knowledge.json\nwindow.KNOWLEDGE = " + js_body + ";\n"
for p in targets_js:
    with open(p, "w", encoding="utf-8") as f:
        f.write(js_text)
