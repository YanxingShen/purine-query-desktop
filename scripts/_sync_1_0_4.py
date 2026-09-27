# -*- coding: utf-8 -*-
"""v1.0.4 导出+同步流水线"""
import json, hashlib, shutil, os

data = open('data/purine-db.json','rb').read()
sha = hashlib.sha256(data).hexdigest()
db = json.loads(data)

# manifest
m = {
    'db_version': '1.0.4',
    'updated': '2026-09-28',
    'item_count': len(db['items']),
    'sha256': sha,
    'update_url': '',
    'release_notes': '1.0.4: 全库准确性复核，合并96条重复/另录条目，统一数值冲突为purine_range，修正类别错误；总条目738->642（去重后），0未知'
}
json.dump(m, open('data/manifest.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

# .js embed
js = 'window.PURINE_DB = ' + json.dumps(db, ensure_ascii=False) + ';'
open('web/data/purine-db.js','w',encoding='utf-8').write(js)
open('desktop/web/data/purine-db.js','w',encoding='utf-8').write(js)

# JSON copies
shutil.copy('data/purine-db.json','web/data/purine-db.json')
shutil.copy('data/purine-db.json','desktop/web/data/purine-db.json')
shutil.copy('data/manifest.json','web/data/manifest.json')
shutil.copy('data/manifest.json','desktop/web/data/manifest.json')

print(f"Synced. Items: {len(db['items'])}, SHA: {sha}")
