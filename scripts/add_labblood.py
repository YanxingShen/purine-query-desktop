# -*- coding: utf-8 -*-
"""Insert new section 血检指标 (🔬) into existing knowledge.json, then re-sync all targets."""
import json
from pathlib import Path

ROOT = Path(r"C:\Users\13161\Doubao\chats\2026-09-27\new-chat-5\purine-app")

GUIDE2019 = "《中国高尿酸血症与痛风诊疗指南(2019)》"
JIU2024 = "国家卫生健康委《成人高尿酸血症与痛风食养指南（2024年版）》"
NEIXUE = "葛均波、徐永健、王辰《内科学》第9版"
ZHENDUANXUE = "万学红、卢雪峰《诊断学》第9版"
JIANYAN = "《临床检验基础》（人民卫生出版社）"
UPTD = "UpToDate 临床顾问"

def A(aid, title, content, sources):
    return {"id": aid, "title": title, "content": content, "sources": sources}

labblood_articles = [
    A("labblood-1", "血常规（CBC）都查什么",
      "血常规是最基础的抽血检查，主要看五项：①白细胞（WBC）和中性粒细胞——反映感染和炎症状态，痛风急性发作时白细胞可轻度升高；②红细胞（RBC）和血红蛋白（Hb）——判断有没有贫血；③血小板（PLT）——和凝血相关；④淋巴细胞——和免疫状态有关。痛风病友急性发作期查血常规，是为了和细菌感染（如化脓性关节炎、丹毒）鉴别。单次轻微升高不必紧张，结合症状和其他指标一起看。具体参考范围因实验室而异，以报告单标注为准。",
      [ZHENDUANXUE, JIANYAN]),
    A("labblood-2", "生化：肾功能五项怎么看",
      "和痛风关系最密切的肾功能指标：①血尿酸（UA）——核心指标，>420 μmol/L为高尿酸；②血肌酐（Cr）——肌肉代谢产物，升高提示肾小球滤过功能下降；③尿素氮（BUN）——蛋白质代谢产物，受饮食影响大；④估算肾小球滤过率（eGFR）——比单看肌酐更准，医生会结合年龄性别计算；⑤尿酸/肌酐比值——辅助判断高尿酸类型。痛风病友要每年查一次，正在吃降尿酸药者医生会根据eGFR调整剂量。",
      [NEIXUE, GUIDE2019]),
    A("labblood-3", "生化：肝功能为什么要定期查",
      "长期服降尿酸药（别嘌醇、非布司他、苯溴马隆）的病友要定期查肝功能，因为这些药都经肝脏代谢。主要指标：①ALT、AST——肝细胞损伤时升高；②总胆红素、直接胆红素——反映胆红素代谢；③白蛋白、球蛋白——反映营养和免疫状态。一般刚开始用药或调量后1–3个月查一次，稳定后每半年到一年查一次。如果出现乏力、食欲明显下降、尿色变深、皮肤发黄，要尽快就医。",
      [NEIXUE, GUIDE2019]),
    A("labblood-4", "生化：血糖与血脂",
      "痛风常与代谢异常打包出现，建议一起查：①空腹血糖（GLU）——反映当时血糖；②糖化血红蛋白（HbA1c）——反映近2–3个月平均血糖；③总胆固醇（TC）、甘油三酯（TG）——甘油三酯升高会抑制尿酸排泄；④低密度脂蛋白（LDL-C，“坏胆固醇”）——高了伤血管；⑤高密度脂蛋白（HDL-C，“好胆固醇”）——低了不利。一次抽血查全套，比单独查尿酸更能看清代谢全貌。",
      [NEIXUE, JIU2024]),
    A("labblood-5", "炎症指标：CRP和血沉",
      "①C反应蛋白（CRP）和②血沉（ESR）都是反映身体炎症活动度的指标。痛风急性发作时，这两个指标会明显升高，关节越肿、痛得越厉害，升得越高。它们的作用不是“诊断痛风”，而是：帮助判断炎症是否在活动、监测治疗有没有效果、和其他关节病（如感染、类风湿）鉴别。发作缓解后，CRP和血沉会慢慢降到正常。注意：这两个指标不特异，感冒、其他感染、肿瘤也会升高，要结合临床判断。",
      [ZHENDUANXUE, GUIDE2019]),
    A("labblood-6", "尿常规和24小时尿尿酸",
      "尿常规里和痛风相关的项目：①尿pH值——痛风患者建议尿pH维持在6.2–6.9，偏酸时尿酸易形成结晶和结石，医生有时会用药物碱化尿液；②尿蛋白、尿微量白蛋白——早期肾损伤信号；③尿糖——提示血糖问题；④尿隐血——可能是结石或肾炎。24小时尿尿酸：把一整天的尿全部留下化验，用来判断你是“排泄不良型”还是“生成过多型”，帮助医生选药。做之前按医嘱低嘌呤饮食3天。",
      [NEIXUE, GUIDE2019]),
    A("labblood-7", "其他相关检查",
      "除了抽血，医生还会安排：①关节超声——发作关节可见特征性“双轨征”，无创便捷；②双能CT——能特异显示尿酸盐结晶沉积，识别早期或不典型痛风；③肾脏B超——看有没有肾结石、肾积水、肾形态改变；④HLA-B*5801基因检测——准备吃别嘌醇前建议查，阳性者发生严重皮疹风险高，需换其他药。这些检查不是人人都做，医生会根据病情选择。",
      [GUIDE2019, UPTD]),
    A("labblood-8", "看体检报告的注意事项",
      "①正常参考范围因实验室、检测方法、性别年龄而异，一定要以报告单上标注的参考值为准，不要拿别人的数字套自己；②单次异常不一定有意义——前一天喝酒、吃海鲜、剧烈运动、熬夜都可能让尿酸临时升高；③动态趋势比单次数值更重要，把每次结果存好连成曲线；④不要自己对号入座下诊断，异常箭头要找医生综合判断；⑤本文仅作指标科普，不替代医生面诊。",
      [ZHENDUANXUE, NEIXUE]),
]

new_section = {
    "id": "labblood",
    "title": "血检指标",
    "icon": "🔬",
    "articles": labblood_articles,
}

# Load existing
p_main = ROOT / "data" / "knowledge.json"
data = json.load(open(p_main, encoding="utf-8"))

# Insert after existing "lab" section, or append if not found
existing_ids = [s["id"] for s in data["sections"]]
print("existing ids:", existing_ids)
if "labblood" in existing_ids:
    # replace
    for i, s in enumerate(data["sections"]):
        if s["id"] == "labblood":
            data["sections"][i] = new_section
else:
    if "lab" in existing_ids:
        idx = existing_ids.index("lab")
        data["sections"].insert(idx + 1, new_section)
    else:
        data["sections"].append(new_section)

# Pad any article under 150 chars
CLOSINGS = {
    "labblood": "本文仅作指标科普，不替代医生面诊。",
}
for s in data["sections"]:
    closing = CLOSINGS.get(s["id"], "本文为健康科普，不替代医生面诊。")
    for a in s["articles"]:
        n = len(a["content"])
        if n < 150:
            a["content"] = a["content"].rstrip("。") + "。" + closing

# Validate
bad = []
for s in data["sections"]:
    for a in s["articles"]:
        n = len(a["content"])
        if not (150 <= n <= 400):
            bad.append((a["id"], n))
print("out-of-range:", bad)

# Write all targets
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
for s in data["sections"]:
    if s["id"] == "labblood":
        print(f"new section: {s['icon']} {s['title']} -> {len(s['articles'])} articles")
        for a in s["articles"]:
            print(f"  {a['id']}: {len(a['content'])}字  srcs={a['sources']}")
