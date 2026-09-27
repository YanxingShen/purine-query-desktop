# -*- coding: utf-8 -*-
import json
db=json.load(open('data/purine-db.json',encoding='utf-8'))
for cat in db['categories']:
    items=[it for it in db['items'] if it['category']==cat]
    print(f'=== {cat} ({len(items)}) ===')
    for it in items:
        v=it['purine_mg_per_100g']
        vstr=str(v) if v is not None else 'NULL'
        print(f"  {it['id']:8s} {it['name']:22s} v={vstr:8s} lvl={it['level']:3s}")
