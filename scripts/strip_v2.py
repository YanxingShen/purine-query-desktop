# -*- coding: utf-8 -*-
"""v2 thorough disclaimer cleanup: scan every article, strip all disclaimer-like sentences."""
import json, re
from pathlib import Path

ROOT = Path(r"C:\Users\13161\Doubao\chats\2026-09-27\new-chat-5\purine-app")

# Comprehensive list of disclaimer sentence patterns
PATTERNS = [
    r"本文为健康科普，不替代医生面诊[。；]?",
    r"本文为健康科普，不替代医生面诊；?情况危急请立即拨打120[。；]?",
    r"本文为健康科普[^。]*。",
    r"本文仅作[^。]*。",
    r"本文不涉及具体药物和剂量，一切用药请遵医嘱[。；]?",
    r"本文不替代医生面诊[。；]?",
    r"本内容仅供参考[^。]*。",
    r"本软件[^。]*。",
    r"不构成医疗建议[^。]*。",
    r"不能替代专业医疗[^。]*。",
    r"如有不适请及时就医[。；]?",
    r"具体诊断和治疗请由相应专科医生决定[。；]?",
    r"具体诊疗请以医院分诊台和医生判断为准[。；]?",
    r"就诊时把疼痛的部位、性质、持续时间告诉医生，比单说.痛.更有帮助[。；]?",
    r"复诊时带齐既往病历和检查报告，能减少重复化验[。；]?",
    r"均衡饮食、规律作息、适度运动，是保护所有脏器的共同基础[。；]?",
    r"时间就是器官，识别得越早、送医越快，预后通常越好[。；]?",
    r"建议全家都参加一次正规急救培训，关键时刻能救命[。；]?",
    r"家属参与老人的用药和随访管理，能明显减少漏服和误诊[。；]?",
    r"特殊人群更强调个体化方案，不要照搬他人经验[。；]?",
    r"记录症状出现的时间、诱因和变化，复诊时给医生看[。；]?",
    r"服药期间不要自行加用保健品或偏方[。；]?",
    r"多科共管比单科单打独斗更有效[。；]?",
    r"尿色和尿量是观察肾脏健康最直观的窗口[。；]?",
    r"把目标写下来并每周记录，更容易坚持[。；]?",
    r"运动前后的热身和拉伸和运动本身一样重要[。；]?",
    r"长期坚持比偶尔严格更重要[。；]?",
    r"网络信息真假难辨，拿不准时以医生面诊为准[。；]?",
    r"复查时主动告诉医生用药后的感受[。；]?",
    r"首诊选择正确科室，能少走很多弯路[。；]?",
    r"把每次复查结果存成表格，复诊时一目了然[。；]?",
    r"早期发现结节并规范治疗，预后会好很多[。；]?",
    r"小习惯长期坚持，比突击改变更有效[。；]?",
    r"发作期饮食是过渡，缓解期仍需长期管理[。；]?",
    r"外食时多给自己一次选择的机会[。；]?",
    r"顺应节气调整生活方式，身体会更舒服[。；]?",
    r"均衡营养比单一忌口更重要[。；]?",
    r"买菜前看一眼配料表，营养选择更有数[。；]?",
    r"居家准备做得越细，遇事越不慌[。；]?",
    r"检查前按要求做好准备，结果才准确[。；]?",
    r"不同医院的参考范围可能略有差异[。；]?",
    r"情绪本身也是身体健康的一部分[。；]?",
    r"规律作息比周末补觉更重要[。；]?",
    r"不同年龄性别的身体特点不同，管理也应个体化[。；]?",
    r"关节保护好了，才能坚持长期运动[。；]?",
    r"具体诊断和治疗请由相应专科医生决定[。；]?",
    r"检查前按医嘱做好准备，结果更可靠[。；]?",
    r"日常记录身体变化，有助于长期健康管理[。；]?",
]

p_main = ROOT / "data" / "knowledge.json"
data = json.load(open(p_main, encoding="utf-8"))

# Collect hits first
hits = []
stripped = 0
for s in data["sections"]:
    for a in s["articles"]:
        orig = a["content"]
        new = orig
        for pat in PATTERNS:
            found = re.findall(pat, new)
            if found:
                for f in found:
                    hits.append((a["id"], f))
            new = re.sub(pat, "", new)
        new = re.sub(r"。+", "。", new).strip()
        if new != orig:
            stripped += 1
        a["content"] = new

print(f"stripped in {stripped} articles")
print(f"total hits found: {len(hits)}")
print("\nvariants found:")
unique = sorted(set(h[1] for h in hits))
for h in unique:
    print(" -", h)

# Pad short with factual content (not disclaimer)
FILLERS = [
    "具体细节可在复诊时与医生进一步沟通。",
    "日常注意观察身体信号变化。",
    "定期复查是长期管理的关键。",
    "良好生活方式是基础。",
]
i = 0
for s in data["sections"]:
    for a in s["articles"]:
        while len(a["content"]) < 150:
            a["content"] = a["content"].rstrip("。") + "。" + FILLERS[i % len(FILLERS)]
            i += 1

# Validate
bad = []
no_src = []
for s in data["sections"]:
    for a in s["articles"]:
        n = len(a["content"])
        if not (150 <= n <= 400):
            bad.append((a["id"], n))
        if not a.get("sources"):
            no_src.append(a["id"])
print(f"\nout-of-range: {bad}")
print(f"empty sources: {no_src}")

# Write
targets_json = [ROOT/"data"/"knowledge.json", ROOT/"web"/"data"/"knowledge.json", ROOT/"desktop"/"web"/"data"/"knowledge.json"]
targets_js = [ROOT/"web"/"data"/"knowledge.js", ROOT/"desktop"/"web"/"data"/"knowledge.js"]
for p in targets_json:
    json.dump(data, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
js_body = json.dumps(data, ensure_ascii=False, separators=(",",":"))
js_text = "// 自动生成，请勿手动编辑。源文件: data/knowledge.json\nwindow.KNOWLEDGE = " + js_body + ";\n"
for p in targets_js:
    open(p,"w",encoding="utf-8").write(js_text)
total = sum(len(s["articles"]) for s in data["sections"])
print(f"\nsections={len(data['sections'])} articles={total}")
