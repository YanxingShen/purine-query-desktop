# 嘌呤数据库 Schema 规范（唯一数据源，两端共用）

## 文件位置
- `data/purine-db.json` — 主数据库（唯一数据源）
- `data/purine-db.xlsx` — 可读表格（由 JSON 导出，便于人工核验）
- `data/manifest.json` — 版本与更新清单

## purine-db.json 顶层结构
```json
{
  "schema_version": "1.0",
  "db_version": "1.0.0",
  "updated": "2026-09-27",
  "unit": "mg/100g 可食部（生重，特殊标注除外）",
  "level_definition": {
    "低": "<75 mg/100g，急性期可适量",
    "中": "75–150 mg/100g，缓解期限量",
    "高": "150–300 mg/100g，尽量避免",
    "极高": ">300 mg/100g，严格禁止"
  },
  "categories": ["谷薯类","豆类及制品","蔬菜类","菌藻类","水果类","坚果种子","畜禽肉类","水产类","蛋类","奶类及制品","饮料","调味品","加工食品","其他"],
  "items": [ ... ]
}
```

## items 单条字段
| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 | 唯一编号，如 G001（G=谷薯），全局不重复 |
| name | string | 是 | 标准食物名 |
| aliases | string[] | 否 | 别名/俗称，用于搜索 |
| category | string | 是 | 大类，必须在 categories 列表内 |
| subcategory | string | 否 | 小类，如"谷类""叶菜类" |
| purine_mg_per_100g | number\|null | 是 | 嘌呤含量，无可靠数据时为 null 并在 note 说明 |
| purine_range | [number,number] | 否 | 不同来源数值范围；单值时两数相同 |
| level | string | 是 | 低/中/高/极高，按 level_definition 判定；null 值标"未知" |
| preparation | string | 否 | 食用部位/加工状态，如"生重/可食部""干重""煮熟" |
| sources | string[] | 是 | 参考来源，至少 1 条，写明书名/指南名/网址 |
| note | string | 否 | 备注，如"因来源而异""痛风急性期慎用" |

## 硬约束
1. 每条必须有 sources，禁止凭空编造数值。
2. 不同文献数值有出入时用 purine_range 并在 note 标"因来源而异"。
3. id 全局唯一，按大类前缀编号。
4. 目标条目数 ≥ 300，覆盖全部 14 个大类。
5. 等级由 purine_mg_per_100g 自动判定，不得手动错配。

## manifest.json 结构
```json
{
  "db_version": "1.0.0",
  "updated": "2026-09-27",
  "item_count": 0,
  "sha256": "<purine-db.json 的 SHA-256>",
  "update_url": "",
  "release_notes": ""
}
```

## knowledge.json 结构（痛风小知识库）
```json
{
  "version": "1.0.0",
  "sections": [
    {
      "id": "cause",
      "title": "病因与机制",
      "icon": "🧬",
      "articles": [
        {"id":"cause-1","title":"...","content":"...","sources":["..."]}
      ]
    }
  ],
  "disclaimer": "本软件仅供健康参考，不替代专业医疗诊断与治疗建议..."
}
```
建议 sections：病因与机制、诱因与分期、饮食红绿灯、常见误区、就医提示、用药常识、生活方式。每节 2–4 篇，内容简明准确，标注来源。
