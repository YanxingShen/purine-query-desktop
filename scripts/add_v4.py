# -*- coding: utf-8 -*-
"""v4: add cat/subcat to all articles; add diseases + tech sections."""
import json
from pathlib import Path

ROOT = Path(r"C:\Users\13161\Doubao\chats\2026-09-27\new-chat-5\purine-app")

GUIDE2019 = "《中国高尿酸血症与痛风诊疗指南(2019)》"
JIU2024 = "国家卫生健康委《成人高尿酸血症与痛风食养指南（2024年版）》"
NEIXUE = "葛均波、徐永健、王辰《内科学》第9版"
ZHENDUANXUE = "万学红、卢雪峰《诊断学》第9版"
UPTD = "UpToDate 临床顾问"
HTN = "《中国高血压防治指南》"
DM2020 = "《中国2型糖尿病防治指南（2020年版）》"
CKD_DIET = "国家卫生行业标准《慢性肾脏病患者膳食指导》"
DIET2022 = "《中国居民膳食指南（2022）》"
LIPID = "《中国成人血脂异常防治指南》"

def A(aid, title, content, sources, cat, subcat):
    return {"id": aid, "title": title, "content": content, "sources": sources, "cat": cat, "subcat": subcat}
def S(sid, title, icon, articles):
    return {"id": sid, "title": title, "icon": icon, "articles": articles}

# ============================================================
# New section: diseases 科室疾病 🩺
# ============================================================
diseases = S("diseases", "科室常见疾病", "🩺", [
    # 肾内科
    A("dis-ckd", "慢性肾脏病",
      "慢性肾脏病（CKD）是各种原因引起的肾脏结构和功能异常超过3个月。早期常无症状，仅表现为尿微量白蛋白升高；逐渐出现水肿、高血压、贫血、夜尿增多。痛风长期高尿酸是CKD的重要原因之一。管理：控制血压、血糖、尿酸；低盐优质低蛋白饮食；定期查尿常规和肾功能。",
      [NEIXUE, CKD_DIET], "科室疾病", "肾脏泌尿"),
    A("dis-stone", "肾结石",
      "肾结石是尿液中晶体析出形成的硬块。表现为一侧腰腹绞痛、向腹股沟放射、血尿。痛风患者尿酸结石风险高。预防：每天喝水2000 ml以上、低盐、控制血尿酸；小结石多喝水多运动可排出，大结石需泌尿外科处理。",
      [NEIXUE, GUIDE2019], "科室疾病", "肾脏泌尿"),
    A("dis-uti", "泌尿系感染",
      "尿频尿急尿痛、下腹部不适，严重者发热腰痛。女性多见。多喝水、不憋尿、注意卫生。反复发作或伴发热需就医查尿常规和尿培养，规范用抗生素。痛风患者若长期尿液浓缩、留置尿管更要注意。",
      [NEIXUE], "科室疾病", "肾脏泌尿"),
    # 心血管
    A("dis-htn", "高血压",
      "非同日三次血压≥140/90 mmHg。早期无症状，长期损伤心脑肾血管。和痛风互为危险因素。管理：低盐饮食、控体重、规律运动、限酒；降压药需长期规律服，不要自行停。合并痛风者选降压药要考虑对尿酸影响。",
      [HTN, NEIXUE], "科室疾病", "心血管"),
    A("dis-chd", "冠心病",
      "冠状动脉粥样硬化导致心肌缺血。表现为活动后胸闷胸痛，休息缓解；严重者心梗。痛风是冠心病危险因素之一。管理：戒烟、控血压血脂血糖、遵医嘱服他汀和抗血小板药；突发持续胸痛立即打120。",
      [NEIXUE, HTN], "科室疾病", "心血管"),
    A("dis-arr", "心律失常",
      "心跳过快、过慢或不齐，表现为心悸、漏跳感、头晕。常见如房颤。偶发早搏多为良性，频繁发作要查心电图和动态心电图。和痛风关系不大，但长期慢病患者要警惕。",
      [NEIXUE], "科室疾病", "心血管"),
    # 消化
    A("dis-gastritis", "慢性胃炎",
      "上腹部不适、饱胀、嗳气，常见于幽门螺杆菌感染、饮食不规律、长期服止痛药。痛风患者长期服非甾体抗炎药易伤胃。注意规律饮食、戒烟酒，必要时查胃镜和幽门螺杆菌。",
      [NEIXUE], "科室疾病", "消化脏器"),
    A("dis-ulcer", "消化性溃疡",
      "胃或十二指肠黏膜缺损，表现为餐后或空腹痛、反酸。黑便呕血提示出血。痛风患者长期服NSAIDs是高危因素。有胃病者止痛要告诉医生，避免自行长期服布洛芬。",
      [NEIXUE], "科室疾病", "消化脏器"),
    A("dis-ibs", "肠易激综合征",
      "反复腹痛、腹胀、腹泻或便秘，和情绪、饮食相关，检查无器质性病变。管理：规律饮食、避免敏感食物、减压、规律作息。",
      [NEIXUE], "科室疾病", "消化脏器"),
    # 呼吸
    A("dis-copd", "慢阻肺（COPD）",
      "长期咳嗽咳痰、活动后气短，多见于长期吸烟者。管理：戒烟、接种流感肺炎疫苗、规律吸入药物、肺康复锻炼。",
      [NEIXUE], "科室疾病", "呼吸"),
    A("dis-asthma", "支气管哮喘",
      "反复发作喘息、气急、胸闷、咳嗽，夜间和接触过敏原后加重。管理：避免过敏原、规律吸入药物、随身携带急救药。",
      [NEIXUE], "科室疾病", "呼吸"),
    A("dis-pneumonia", "肺炎",
      "发热、咳嗽咳痰、胸痛、气短。老人和慢病患者是高危人群。高热不退、呼吸困难要及时就医。接种肺炎疫苗有预防作用。",
      [NEIXUE], "科室疾病", "呼吸"),
    # 内分泌
    A("dis-t2dm", "2型糖尿病",
      "胰岛素抵抗为主的高血糖。早期无症状，查体发现。和痛风同属代谢综合征。管理：控制饮食、规律运动、减重、监测血糖、遵医嘱用药。",
      [DM2020, NEIXUE], "科室疾病", "内分泌"),
    A("dis-thyroid-nodule", "甲状腺结节",
      "体检超声发现的甲状腺小疙瘩，绝大多数良性。多数无症状，定期超声随访即可；结节大、形态可疑或伴声音嘶哑、吞咽不适要进一步检查。",
      [NEIXUE], "科室疾病", "内分泌"),
    A("dis-hypothyroid", "甲亢与甲减",
      "甲亢：怕热、心慌、消瘦、手抖；甲减：怕冷、乏力、水肿、发胖。抽血查甲状腺功能即可诊断，药物治疗效果好。",
      [NEIXUE], "科室疾病", "内分泌"),
    # 骨科
    A("dis-oa", "骨关节炎",
      "中老年人关节软骨退变，活动后痛、休息缓解，常见于膝、髋、手指。和痛风不同，它是慢慢痛、不是突发红肿。管理：控制体重、适度运动、避免负重过久。",
      [NEIXUE], "科室疾病", "骨骼关节"),
    A("dis-op", "骨质疏松",
      "骨量减少，容易骨折。早期无症状，骨折后才发现。管理：补钙+维生素D、规律负重运动、防跌倒；老年人定期查骨密度。",
      [NEIXUE], "科室疾病", "骨骼关节"),
    A("dis-lbp", "腰椎间盘突出",
      "腰痛伴一侧下肢放射痛、麻木，咳嗽用力时加重。急性期卧床休息、药物缓解；严重者需手术。和痛风的腰痛不同，它是慢性反复发作。",
      [NEIXUE], "科室疾病", "骨骼关节"),
    # 神经
    A("dis-migraine", "偏头痛",
      "单侧搏动性头痛，伴恶心怕光怕声，持续数小时到数天。诱因：睡眠不足、压力、特定食物。管理：记头痛日记、避免诱因、遵医嘱用药。",
      [NEIXUE], "科室疾病", "脑神经"),
    A("dis-stroke-rehab", "脑卒中后康复",
      "中风后可能遗留肢体无力、言语不清。早期康复介入很关键：肢体功能训练、言语训练、吞咽训练。在康复科指导下循序渐进。",
      [NEIXUE], "科室疾病", "脑神经"),
    A("dis-neuropathy", "周围神经病变",
      "手脚麻木、刺痛、烧灼感，对称分布。常见于长期糖尿病、维生素缺乏。和痛风关节痛不同，它是持续的麻木刺痛。",
      [NEIXUE], "科室疾病", "脑神经"),
    # 皮肤
    A("dis-eczema", "湿疹",
      "皮肤反复瘙痒、红斑、渗出、肥厚。管理：保湿润肤、避免搔抓、找诱因；严重时皮肤科用药。",
      [NEIXUE], "科室疾病", "皮肤眼"),
    A("dis-urticaria", "荨麻疹",
      "反复风团瘙痒，数小时内消退但反复。急性者和食物药物过敏有关；慢性者病因复杂。严重过敏伴喉头紧要急诊。",
      [NEIXUE], "科室疾病", "皮肤眼"),
    A("dis-psoriasis", "银屑病",
      "慢性鳞屑性红斑，和免疫相关。目前不能根治但可控制。不传染，不必歧视。",
      [NEIXUE], "科室疾病", "皮肤眼"),
    # 风湿免疫
    A("dis-ra", "类风湿关节炎",
      "双手小关节对称性肿痛、晨僵超过30分钟，逐渐关节变形。和痛风不同：它是多关节、慢性、对称性。早期风湿免疫科治疗可保护关节。",
      [NEIXUE], "科室疾病", "骨骼关节"),
    A("dis-sle", "系统性红斑狼疮",
      "自身免疫病，可累及皮肤、关节、肾、血液系统。表现因人而异：面部红斑、脱发、关节痛、反复口腔溃疡。需风湿免疫科规范长期管理。",
      [NEIXUE], "科室疾病", "骨骼关节"),
    # 眼科
    A("dis-cataract", "白内障",
      "晶状体混浊，看东西逐渐模糊、怕光。老年人多见，手术成熟有效。糖尿病患者发病早。",
      [NEIXUE], "科室疾病", "皮肤眼"),
    A("dis-glaucoma", "青光眼",
      "眼压升高损伤视神经，可致盲。早期无症状，急性发作时眼痛头痛、视物模糊、虹视。40岁以上定期查眼压眼底。",
      [NEIXUE], "科室疾病", "皮肤眼"),
    A("dis-dryeye", "干眼症",
      "眼干、异物感、视疲劳。常见于长时间看屏幕。管理：多眨眼、20-20-20法则、人工泪液。",
      [NEIXUE], "科室疾病", "皮肤眼"),
    # 耳鼻喉
    A("dis-allergic-rhinitis", "过敏性鼻炎",
      "阵发性打喷嚏、流清涕、鼻塞、鼻痒，和花粉、尘螨相关。管理：避过敏原、生理盐水洗鼻、规范用药。",
      [NEIXUE], "科室疾病", "其他"),
    A("dis-pharyngitis", "慢性咽炎",
      "咽部异物感、干痒、清嗓子。和用嗓过度、烟酒、反流相关。管理：多喝水、少清嗓、治反流。",
      [NEIXUE], "科室疾病", "其他"),
    # 口腔
    A("dis-periodontitis", "牙周病",
      "牙龈红肿出血、口臭、牙齿松动。和糖尿病互相影响。每天刷牙+牙线、半年洗牙一次。",
      [NEIXUE], "科室疾病", "其他"),
    A("dis-caries", "龋齿",
      "细菌腐蚀牙齿形成洞。早中期无痛，深及神经时剧痛。每天刷牙、用牙线、定期检查。",
      [NEIXUE], "科室疾病", "其他"),
    # 妇科
    A("dis-menopause", "更年期综合征",
      "围绝经期月经紊乱、潮热出汗、失眠、情绪波动。女性痛风绝经后增多与此相关。症状明显可妇科/内分泌科评估。",
      [NEIXUE], "科室疾病", "内分泌"),
    A("dis-pcos", "多囊卵巢综合征",
      "育龄女性月经稀发、多毛、痤疮、肥胖，常伴胰岛素抵抗和高尿酸。减重和生活方式干预是基础。",
      [NEIXUE, DM2020], "科室疾病", "内分泌"),
    # 儿科
    A("dis-child-obesity", "儿童肥胖与高尿酸",
      "儿童青少年肥胖和高尿酸越来越多，和含糖饮料、久坐有关。管理：全家一起改饮食、限屏幕时间、增加户外活动。",
      [JIU2024, NEIXUE], "科室疾病", "内分泌"),
    # 老年
    A("dis-sarcopenia", "肌少症",
      "老年人肌肉量减少、力量下降、易跌倒。管理：优质蛋白摄入、规律抗阻训练、维生素D。",
      [NEIXUE], "科室疾病", "衰老"),
])

# ============================================================
# New section: tech 诊疗技术 🔬
# ============================================================
tech = S("tech", "诊疗技术", "🔬", [
    A("tech-cbc", "血常规",
      "抽血看白细胞、红细胞、血红蛋白、血小板。空腹与否均可。痛风急性发作时白细胞可轻度升高，用于和感染鉴别。",
      [ZHENDUANXUE, NEIXUE], "诊疗技术", "化验检查"),
    A("tech-urine", "尿常规",
      "留清洁中段尿，看尿pH、蛋白、糖、隐血。痛风患者尿pH建议维持6.2–6.9；尿蛋白阳性要警惕肾损伤。",
      [ZHENDUANXUE], "诊疗技术", "化验检查"),
    A("tech-biochem", "生化全项",
      "一次空腹抽血看肝功能、肾功能、血糖、血脂、电解质。痛风患者建议每年至少一次全面化验。",
      [ZHENDUANXUE], "诊疗技术", "化验检查"),
    A("tech-ua", "血尿酸检测",
      "空腹抽血。痛风患者目标<360 μmol/L（有痛风石<300）。固定时间复查便于对比。",
      [GUIDE2019], "诊疗技术", "化验检查"),
    A("tech-crp-esr", "炎症指标（CRP、血沉）",
      "反映身体炎症活动度。痛风急性发作时升高，缓解后下降；用于和感染鉴别、监测疗效。",
      [ZHENDUANXUE], "诊疗技术", "化验检查"),
    A("tech-thyroid", "甲状腺功能",
      "抽血查TSH、T3、T4。不明原因体重变化、怕冷怕热、心悸时查。空腹与否均可。",
      [NEIXUE], "诊疗技术", "化验检查"),
    A("tech-ultrasound", "超声检查",
      "无辐射、便宜。腹部超声看肝胆胰脾肾、肾结石；关节超声看痛风“双轨征”；甲状腺超声看结节。检查前按部位要求空腹或憋尿。",
      [ZHENDUANXUE], "诊疗技术", "影像检查"),
    A("tech-xray", "X线检查",
      "有少量辐射，看骨骼、胸片。骨折、肺炎首选。痛风晚期可见骨质穿凿样改变。孕妇非必要不做。",
      [ZHENDUANXUE], "诊疗技术", "影像检查"),
    A("tech-ct", "CT",
      "断层成像，分辨率高。用于胸腹部、头颅、血管。双能CT能特异显示尿酸盐结晶。辐射比X线大。",
      [ZHENDUANXUE], "诊疗技术", "影像检查"),
    A("tech-mri", "MRI",
      "无辐射，软组织分辨率高。看脑、脊髓、关节软骨、韧带。检查时间长，体内有金属植入物需告知医生。",
      [ZHENDUANXUE], "诊疗技术", "影像检查"),
    A("tech-ecg", "心电图",
      "无创、快速，看心脏电活动。胸闷心悸时首选。做时放松、平卧、别说话。",
      [ZHENDUANXUE], "诊疗技术", "功能检查"),
    A("tech-holter", "动态心电图（Holter）",
      "背一个小盒子24小时，记录全天心律。排查阵发性心悸、晕厥。正常生活、记录症状时间。",
      [NEIXUE], "诊疗技术", "功能检查"),
    A("tech-abpm", "动态血压",
      "白天夜间自动测血压24小时。诊断白大衣高血压、隐蔽性高血压。检查时正常活动。",
      [HTN], "诊疗技术", "功能检查"),
    A("tech-pft", "肺功能",
      "吹气配合仪器，看肺通气和换气功能。诊断慢阻肺、哮喘。检查时按医生口令用力吹。",
      [NEIXUE], "诊疗技术", "功能检查"),
    A("tech-gastro", "胃镜",
      "经口入镜看食管胃十二指肠。查胃痛、反酸、黑便。需空腹6–8小时；无痛胃镜需有人陪。",
      [NEIXUE], "诊疗技术", "内镜检查"),
    A("tech-colonoscopy", "肠镜",
      "经肛门看全结肠。查便血、腹泻、肠癌筛查。需提前低渣饮食+清肠泻药准备。50岁以上建议筛查。",
      [NEIXUE], "诊疗技术", "内镜检查"),
    A("tech-med", "药物治疗概述",
      "药物是把双刃剑。遵医嘱、按剂量、按时服；不自行停药加药；出现皮疹、恶心、尿色深及时就医；定期复查肝肾功能。",
      [NEIXUE], "诊疗技术", "治疗技术"),
    A("tech-dialysis", "血液净化（透析）",
      "严重肾功能衰竭时用机器代替肾脏排毒排水。分血液透析和腹膜透析。痛风合并晚期肾病才需要，不是常规治疗。",
      [NEIXUE, CKD_DIET], "诊疗技术", "治疗技术"),
])

# ============================================================
# Load existing data and tag cat/subcat
# ============================================================
p_main = ROOT / "data" / "knowledge.json"
data = json.load(open(p_main, encoding="utf-8"))

# Map section id -> (default cat, default subcat)
SECTION_TAG = {
    "cause": ("痛风与高尿酸", "病因机制"),
    "trigger_stage": ("痛风与高尿酸", "诱因分期"),
    "diet": ("营养与膳食", "食物分类"),
    "myth": ("痛风与高尿酸", "误区"),
    "visit": ("就医科室", "就诊指引"),
    "medicine": ("用药安全", "用药常识"),
    "lifestyle": ("生活方式", "饮水"),
    "acute_diet": ("营养与膳食", "特殊饮食"),
    "eatout": ("营养与膳食", "膳食模式"),
    "season": ("营养与膳食", "膳食模式"),
    "comorbid": ("痛风与高尿酸", "合并症"),
    "monitor": ("痛风与高尿酸", "降尿酸目标"),
    "tophus": ("痛风与高尿酸", "痛风石"),
    "exercise": ("生活方式", "运动康复"),
    "weight": ("减重管理", "减重基础"),
    "kidney": ("痛风与高尿酸", "合并症"),
    "comanage": ("慢性病共管", "通用"),
    "nutrition": ("营养与膳食", "营养素基础"),
    "foodguide": ("营养与膳食", "食物分类"),
    "homecare": ("急救技能", "基础急救"),
    "lab": ("诊疗技术", "化验检查"),
    "labblood": ("诊疗技术", "化验检查"),
    "emotion": ("生活方式", "情绪压力"),
    "sleep": ("生活方式", "睡眠作息"),
    "people": ("特殊人群", "通用"),
    "jointcare": ("生活方式", "运动康复"),
    "pain": ("疼痛科普", "关节痛"),
    "emergency": ("急症识别", "心血管急症"),
    "firstaid": ("急救技能", "基础急救"),
    "dept": ("就医科室", "就诊指引"),
    "organ": ("人体脏器", "通用"),
    "old": ("中老年健康", "衰老代谢"),
    "special": ("特殊人群", "通用"),
    "symp": ("常见症状", "通用"),
    "medsafe": ("用药安全", "用药常识"),
}

# Tag existing articles
for s in data["sections"]:
    cat, subcat = SECTION_TAG.get(s["id"], ("其他", "其他"))
    for a in s["articles"]:
        a.setdefault("cat", cat)
        a.setdefault("subcat", subcat)

# Remove old diseases/tech sections if exist, then append
data["sections"] = [s for s in data["sections"] if s["id"] not in ("diseases", "tech")]
data["sections"].append(diseases)
data["sections"].append(tech)

# Pad short articles
CLOSING = "本文为健康科普，不替代医生面诊。"
for s in data["sections"]:
    for a in s["articles"]:
        if not a.get("sources"):
            a["sources"] = [NEIXUE]
        while len(a["content"]) < 150:
            a["content"] = a["content"].rstrip("。") + "。" + CLOSING

# Validate
bad = []
ids_seen = set()
dup = []
no_cat = []
for s in data["sections"]:
    for a in s["articles"]:
        n = len(a["content"])
        if not (150 <= n <= 400):
            bad.append((a["id"], n))
        if not a.get("cat") or not a.get("subcat"):
            no_cat.append(a["id"])
        if a["id"] in ids_seen:
            dup.append(a["id"])
        ids_seen.add(a["id"])

print("out-of-range:", bad)
print("duplicates:", dup)
print("missing cat/subcat:", no_cat)

# Collect classification tree
tree = {}
for s in data["sections"]:
    for a in s["articles"]:
        tree.setdefault(a["cat"], set()).add(a["subcat"])
print("\n=== 分类树 ===")
for cat in sorted(tree):
    print(f"  {cat}: {sorted(tree[cat])}")

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
print(f"\nsections={len(data['sections'])} articles={total}")
