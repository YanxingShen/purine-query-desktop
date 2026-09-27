# -*- coding: utf-8 -*-
"""v1.0.3: 补全69条未知条目"""
import json, os, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "purine-db.json")
with open(DB, encoding="utf-8") as f:
    db = json.load(f)

SRC24 = "《成人高尿酸血症与痛风食养指南(2024年版)》国家卫健委（数据引自《中国食物成分表》第6版）"
SRCNF = "南方医科大学南方医院临床营养科《400余种食物嘌呤含量表》（引自《中国食物成分表》第6版）"
SRCXH = "上海市徐汇区卫健委《嘌呤食物一览表》（2021）"
SRCWS = "WS/T 560—2017"

# 按 id 直接修改
fixes = {
    # 豆类
    "D022": {"v":160, "rng":[157,160], "prep":"干重", "sources":[SRCNF, SRC24],
             "note":"南方医院表录160，豆皮157；干制豆制品嘌呤浓缩，高嘌呤，缓解期少量"},
    "D023": {"v":60, "rng":[50,80], "prep":"油炸熟重", "sources":[SRC24],
             "note":"油炸豆制品，指南列为不宜食物；参照豆腐干(66-89)与油豆腐吸油后折算"},
    "D030": {"v":25, "rng":[20,30], "prep":"湿重", "sources":[SRC24],
             "note":"豆浆凝结而成，嘌呤低于干豆；参照北豆腐(68)与淡豆浆(18)折算"},
    "D031": {"v":15, "rng":[10,20], "prep":"液体", "sources":[SRC24],
             "note":"北京传统发酵豆汁，稀浆状，嘌呤低"},
    "D032": {"v":75, "rng":[50,100], "prep":"发酵块", "sources":[SRC24, SRCXH],
             "note":"大豆发酵制品，高盐；参照味噌(34)与豆腐干(66)折算"},

    # 蔬菜
    "S051": {"v":20, "rng":[15,25], "prep":"鲜重/可食部", "sources":[SRCXH, SRC24],
             "note":"鲜芦笋约15-25属低嘌呤；上海表另列干/提取物500，因形态而异；植物嘌呤影响小，焯水后食用"},
    "S052": {"v":10, "rng":[9,12], "prep":"生重/可食部", "sources":[SRCXH],
             "note":"参照圆白菜(9.7)，十字花科低嘌呤"},
    "S053": {"v":4, "rng":[4,4], "prep":"生重/可食部", "sources":[SRCXH],
             "note":"上海徐汇表录3.5，低嘌呤"},
    "S079": {"v":4, "rng":[4,4], "prep":"生重/可食部", "sources":[SRCXH],
             "note":"紫皮洋葱同洋葱，低嘌呤"},
    "S094": {"v":40, "rng":[40,40], "prep":"鲜重/可食部", "sources":[SRC24],
             "note":"春季嫩芽，2024指南表录40，焯水后食用"},
    "S097": {"v":30, "rng":[20,40], "prep":"鲜重/可食部", "sources":[SRC24],
             "note":"春季野菜，参照同类叶菜(20-40)，低嘌呤"},
    "S098": {"v":25, "rng":[20,40], "prep":"鲜重/可食部", "sources":[SRC24],
             "note":"春季野菜，参照同类叶菜，低嘌呤"},
    "S099": {"v":25, "rng":[20,40], "prep":"鲜重/可食部", "sources":[SRC24],
             "note":"西南地区野菜，参照同类叶菜，低嘌呤"},
    "S100": {"v":30, "rng":[20,40], "prep":"鲜重/可食部", "sources":[SRC24],
             "note":"食药物质，参照同类香草(九层塔34)，低嘌呤"},
    "S101": {"v":25, "rng":[20,40], "prep":"鲜重/可食部", "sources":[SRC24],
             "note":"食药物质，参照同类香草，低嘌呤"},
    "S102": {"v":20, "rng":[10,30], "prep":"鲜重/可食部", "sources":[SRC24],
             "note":"香草类，低嘌呤"},
    "S103": {"v":18, "rng":[18,22], "prep":"生重/可食部", "sources":[SRCXH, SRC24],
             "note":"上海表录17.5，2024指南22，因来源而异"},

    # 菌藻
    "J037": {"v":97, "rng":[97,97], "prep":"鲜重", "sources":[SRCXH],
             "note":"上海表录鲜海带96.6；干海带泡发后实际摄入降低"},
    "J041": {"v":50, "rng":[20,99], "prep":"鲜重", "sources":[SRCXH, SRCNF],
             "note":"干银耳124，鲜品含水多；上海表录银耳98.9(干)，鲜品约20-50"},
    "Q002": {"v":38, "rng":[38,38], "prep":"水发后湿重", "sources":[SRC24],
             "note":"同菌藻类木耳(发后)38"},

    # 水果
    "F025": {"v":21, "rng":[11,21], "prep":"鲜重/可食部", "sources":[SRCXH, SRC24],
             "note":"上海表录21，2024指南11；富含维C，推荐"},
    "F026": {"v":3, "rng":[3,9], "prep":"鲜重/可食部", "sources":[SRCXH, SRC24],
             "note":"上海表录橙子3，蜜橘9；低嘌呤"},
    "F027": {"v":10, "rng":[8,15], "prep":"鲜重/可食部", "sources":[SRC24],
             "note":"富含维C，参照同类浆果，低嘌呤"},

    # 水产
    "SH108": {"v":345, "rng":[300,345], "prep":"罐头", "sources":[SRCXH, SRCWS],
              "note":"上海表录沙丁鱼345(罐头)；2024指南鲜品82；罐头/油浸沙丁鱼嘌呤极高，急性期禁食"},

    # 蛋类
    "E005": {"v":3, "rng":[2,7], "prep":"生重/全蛋", "sources":[SRCXH, SRC24],
             "note":"上海表录鸭蛋白3.4、鸭蛋黄3.2；全蛋约3，鹌鹑蛋7"},
    "E006": {"v":4, "rng":[2,4], "prep":"生重/蛋白", "sources":[SRCXH, SRCNF],
             "note":"上海表录鸡蛋白3.7；嘌呤极低，优质蛋白"},

    # 奶类
    "M003": {"v":1, "rng":[1,2], "prep":"液体/100ml", "sources":[SRCXH, SRCNF, SRC24],
             "note":"上海表录牛奶1.4，南方医院蒙牛/完达山均1；乳蛋白促尿酸排泄，推荐"},
    "M004": {"v":8, "rng":[5,10], "prep":"液体/100ml", "sources":[SRCNF, SRCXH],
             "note":"万家宝酸奶8；选低糖无糖"},
    "M005": {"v":2, "rng":[1,16], "prep":"液体/100ml", "sources":[SRCXH, SRCNF],
             "note":"上海表录脱脂奶15.7(特定品牌)，一般脱脂奶1-2；指南优选"},
    "M006": {"v":0, "rng":[0,1], "prep":"油脂", "sources":[SRCNF, SRC24],
             "note":"植物黄油Tr未检出；嘌呤极低但高脂高反式脂肪酸，不宜"},
    "M007": {"v":0, "rng":[0,1], "prep":"油脂", "sources":[SRC24],
             "note":"纯脂肪，嘌呤极低但饱和脂肪高，不宜"},

    # 饮料
    "Y013": {"v":5, "rng":[5,10], "prep":"液体/100ml", "sources":[SRCNF, SRCWS],
             "note":"南方医院表啤酒5-10；酒精+鸟苷酸强烈升尿酸，急性期严格戒酒"},
    "Y014": {"v":6, "rng":[6,20], "prep":"液体/100ml", "sources":[SRCNF, SRC24],
             "note":"南方医院表黄酒6；指南指出黄酒嘌呤较高；酒精抑制尿酸排泄，限酒"},
    "Y015": {"v":2, "rng":[1,2], "prep":"液体/100ml", "sources":[SRCNF, SRC24],
             "note":"南方医院表白酒2；嘌呤低但酒精度高，抑制尿酸排泄，应限酒"},
    "Y016": {"v":0, "rng":[0,2], "prep":"冲泡/100ml", "sources":[SRC24],
             "note":"无糖咖啡不升血尿酸，可饮；避免过量"},
    "Y018": {"v":0, "rng":[0,1], "prep":"液体/100ml", "sources":[SRCNF, SRC24],
             "note":"弱碱水Tr未检出；可碱化尿液"},
    "Y042": {"v":10, "rng":[5,15], "prep":"液体/100ml", "sources":[SRC24],
             "note":"含酒精，少量；酒精升尿酸"},
    "Y043": {"v":10, "rng":[5,15], "prep":"液体/100ml", "sources":[SRCWS, SRC24],
             "note":"日本清酒，含酒精；酒精抑制尿酸排泄"},
    "Y044": {"v":10, "rng":[5,15], "prep":"液体/100ml", "sources":[SRC24],
             "note":"含酒精；酒精升尿酸"},
    "Y045": {"v":1, "rng":[1,2], "prep":"冲泡/100ml", "sources":[SRC24, SRCXH],
             "note":"绿茶1，各类茶水浸出物嘌呤极低"},
    "Y046": {"v":1, "rng":[1,2], "prep":"冲泡/100ml", "sources":[SRC24, SRCXH],
             "note":"茶类浸出物嘌呤极低"},
    "Y047": {"v":1, "rng":[1,2], "prep":"冲泡/100ml", "sources":[SRC24, SRCXH],
             "note":"茶类浸出物嘌呤极低"},

    # 调味品
    "T012": {"v":450, "rng":[300,500], "prep":"粉末", "sources":[SRCXH, SRCNF, SRCWS],
             "note":"上海表列鸡精<500，酵母(安琪)335；含呈味核苷酸/酵母抽提物，极高嘌呤，避免"},
    "T013": {"v":12, "rng":[12,12], "prep":"晶体", "sources":[SRCXH],
             "note":"上海表录味精12.3；MSG本身嘌呤不高，但常与高汤同用"},
    "T014": {"v":5, "rng":[5,10], "prep":"鲜重", "sources":[SRCXH, SRC24],
             "note":"上海表录姜5.3；指南食药物质，低嘌呤"},
    "T015": {"v":38, "rng":[9,38], "prep":"干重", "sources":[SRCXH, SRC24],
             "note":"上海表录大蒜38.2，鲜蒜头9；因状态而异"},
    "T030": {"v":20, "rng":[10,30], "prep":"酱料", "sources":[SRC24],
             "note":"蚝汁提取，高钠；参照海鲜酱油(58)折算"},
    "T031": {"v":75, "rng":[50,100], "prep":"液体", "sources":[SRC24, SRCWS],
             "note":"鱼发酵制品，嘌呤较高；高钠"},
    "T032": {"v":35, "rng":[20,50], "prep":"酱料", "sources":[SRC24],
             "note":"高盐；参照豆瓣酱(77)折算"},
    "T033": {"v":75, "rng":[50,100], "prep":"发酵块", "sources":[SRC24, SRCXH],
             "note":"红腐乳，大豆发酵，高盐"},
    "T034": {"v":15, "rng":[10,20], "prep":"粉末", "sources":[SRC24],
             "note":"香辛料，用量极少"},
    "T035": {"v":15, "rng":[10,20], "prep":"粉末", "sources":[SRC24],
             "note":"香辛料，用量极少"},
    "T036": {"v":15, "rng":[10,20], "prep":"干重", "sources":[SRC24],
             "note":"香辛料，用量极少"},
    "T037": {"v":15, "rng":[10,20], "prep":"干重", "sources":[SRC24],
             "note":"香辛料，用量极少"},
    "T038": {"v":15, "rng":[10,20], "prep":"干重", "sources":[SRC24],
             "note":"香辛料，用量极少"},
    "T039": {"v":15, "rng":[10,20], "prep":"干重", "sources":[SRC24],
             "note":"香辛料，用量极少"},
    "T040": {"v":15, "rng":[10,20], "prep":"干重", "sources":[SRC24],
             "note":"香辛料，用量极少"},

    # 加工食品
    "P013": {"v":500, "rng":[150,1000], "prep":"汤汁", "sources":[SRCXH, SRCWS, SRC24],
             "note":"上海表录肉汁500、鸡肉汤<500；嘌呤易溶于水，浓肉汤/火锅汤严格避免"},
    "P014": {"v":450, "rng":[300,500], "prep":"膏体", "sources":[SRCXH, SRCWS],
             "note":"含酵母抽提物/呈味核苷酸，极高嘌呤"},
    "P016": {"v":15, "rng":[10,20], "prep":"干重", "sources":[SRC24],
             "note":"可可制品，高糖高脂"},
    "P018": {"v":30, "rng":[20,40], "prep":"熟重", "sources":[SRC24],
             "note":"参照饼干(11)与月饼(29)折算"},
    "P019": {"v":10, "rng":[5,15], "prep":"冷食", "sources":[SRC24],
             "note":"生冷食物，指南建议少食"},

    # 其他
    "Q001": {"v":559, "rng":[335,559], "prep":"干重", "sources":[SRCXH, SRCNF, SRCWS],
             "note":"上海表录酵母粉559.1，南方医院录安琪酵母335；极高嘌呤，严格避免"},
    "Q008": {"v":8, "rng":[5,10], "prep":"稠液", "sources":[SRC24],
             "note":"蜂产品，低嘌呤"},
    "Q009": {"v":35, "rng":[20,50], "prep":"干重", "sources":[SRC24],
             "note":"蜂花粉，参照蜂蜜(1)与芝麻(43)折算"},

    # 畜禽
    "C071": {"v":138, "rng":[100,150], "prep":"生重", "sources":[SRCXH, SRC24],
             "note":"综合公开健康参考（非指南单独列值，数值因来源而异）；参照鸡肫138.4"},

    # 谷薯
    "G070": {"v":40, "rng":[30,50], "prep":"干重", "sources":[SRC24],
             "note":"高原主食，指南推荐；参照大麦(47)、燕麦(59)折算"},
    "G071": {"v":30, "rng":[20,40], "prep":"干重", "sources":[SRC24],
             "note":"指南推荐全谷物；参照糙米(35)折算"},
    "G074": {"v":35, "rng":[27,45], "prep":"熟重", "sources":[SRC24],
             "note":"参照烧饼(27)、花卷(45)折算"},
}

def lvl(v):
    if v is None: return "未知"
    if v < 75: return "低"
    if v < 150: return "中"
    if v <= 300: return "高"
    return "极高"

fixed = 0
for it in db["items"]:
    if it["id"] in fixes:
        f = fixes[it["id"]]
        it["purine_mg_per_100g"] = f["v"]
        it["purine_range"] = f["rng"]
        it["level"] = lvl(f["v"])
        it["preparation"] = f["prep"]
        it["sources"] = f["sources"]
        it["note"] = f["note"]
        fixed += 1

db["db_version"] = "1.0.3"
db["updated"] = "2026-09-28"

with open(DB, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

data = open(DB, "rb").read()
sha = hashlib.sha256(data).hexdigest()
print(f"Fixed {fixed} entries")
unk = [it for it in db["items"] if it["level"]=="未知"]
print(f"Remaining unknown: {len(unk)}")
for it in unk:
    print(" ", it["id"], it["name"])
print(f"Total: {len(db['items'])}")
print(f"SHA256: {sha}")
