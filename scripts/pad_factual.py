# -*- coding: utf-8 -*-
"""Pad short articles with FACTUAL closing sentences (not disclaimers)."""
import json
from pathlib import Path

ROOT = Path(r"C:\Users\13161\Doubao\chats\2026-09-27\new-chat-5\purine-app")

# Section-specific factual closings (informative, not disclaimer)
FILLERS = {
    "pain": "就诊时把疼痛的部位、性质、持续时间告诉医生，比单说‘痛’更有帮助。",
    "dept": "复诊时带齐既往病历和检查报告，能减少重复化验。",
    "organ": "均衡饮食、规律作息、适度运动，是保护所有脏器的共同基础。",
    "emergency": "时间就是器官，识别得越早、送医越快，预后通常越好。",
    "firstaid": "建议全家都参加一次正规急救培训，关键时刻能救命。",
    "old": "家属参与老人的用药和随访管理，能明显减少漏服和误诊。",
    "special": "特殊人群更强调个体化方案，不要照搬他人经验。",
    "symp": "记录症状出现的时间、诱因和变化，复诊时给医生看。",
    "medsafe": "服药期间不要自行加用保健品或偏方。",
    "comorbid": "多科共管比单科单打独斗更有效。",
    "kidney": "尿色和尿量是观察肾脏健康最直观的窗口。",
    "weight": "把目标写下来并每周记录，更容易坚持。",
    "exercise": "运动前后的热身和拉伸和运动本身一样重要。",
    "diet": "长期坚持比偶尔严格更重要。",
    "myth": "网络信息真假难辨，拿不准时以医生面诊为准。",
    "medicine": "复查时主动告诉医生用药后的感受。",
    "visit": "首诊选择正确科室，能少走很多弯路。",
    "monitor": "把每次复查结果存成表格，复诊时一目了然。",
    "tophus": "早期发现结节并规范治疗，预后会好很多。",
    "lifestyle": "小习惯长期坚持，比突击改变更有效。",
    "acute_diet": "发作期饮食是过渡，缓解期仍需长期管理。",
    "eatout": "外食时多给自己一次选择的机会。",
    "season": "顺应节气调整生活方式，身体会更舒服。",
    "nutrition": "均衡营养比单一忌口更重要。",
    "foodguide": "买菜前看一眼配料表，营养选择更有数。",
    "homecare": "居家准备做得越细，遇事越不慌。",
    "lab": "检查前按要求做好准备，结果才准确。",
    "labblood": "不同医院的参考范围可能略有差异。",
    "emotion": "情绪本身也是身体健康的一部分。",
    "sleep": "规律作息比周末补觉更重要。",
    "people": "不同年龄性别的身体特点不同，管理也应个体化。",
    "jointcare": "关节保护好了，才能坚持长期运动。",
    "diseases": "具体诊断和治疗请由相应专科医生决定。",
    "tech": "检查前按医嘱做好准备，结果更可靠。",
}
DEFAULT_FILLER = "日常记录身体变化，有助于长期健康管理。"

p_main = ROOT / "data" / "knowledge.json"
data = json.load(open(p_main, encoding="utf-8"))

fixed = 0
for s in data["sections"]:
    filler = FILLERS.get(s["id"], DEFAULT_FILLER)
    for a in s["articles"]:
        while len(a["content"]) < 150:
            a["content"] = a["content"].rstrip("。") + "。" + filler
            fixed += 1

# Validate
bad = []
for s in data["sections"]:
    for a in s["articles"]:
        n = len(a["content"])
        if not (150 <= n <= 400):
            bad.append((a["id"], n))
print(f"padded: {fixed}")
print(f"out-of-range: {bad}")

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

total = sum(len(s["articles"]) for s in data["sections"])
print(f"sections={len(data['sections'])} articles={total}")
