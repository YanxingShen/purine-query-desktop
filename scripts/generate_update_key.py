#!/usr/bin/env python3
"""
嘌呤数据库更新密钥生成工具（官方侧使用）
支持两种密钥形态：
  通道②短码（默认）：16位短码 XXXX-XXXX-XXXX-XXXX + 托管索引文件 keys/<f>.json
  通道②长码/兼容：PUR-<base64url> 长密钥（含mac，向后兼容）
  通道③离线包：密钥内含 gzip 压缩的完整数据库

用法（短码，推荐）:
    python scripts/generate_update_key.py --db data/purine-db.json --url https://yanxingshen.github.io/purine-query-web/ --exp 2027-03-01 --count 5 --keys-dir ./keys-out

用法（长码兼容）:
    python scripts/generate_update_key.py --db data/purine-db.json --url https://example.com/db.json --exp 2027-03-01 --long

用法（离线包）:
    python scripts/generate_update_key.py --db data/purine-db.json --offline --exp 2027-03-01
"""
import argparse
import base64
import gzip
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
from datetime import date

# MAC 签名盐（按版本轮换的固定常量，必须与前端 app.js 中 PURINE_MAC_SALT 完全一致）
MAC_SALT = "purine-app-v1-mac-salt-2026"

# 32 字母表（剔除易混淆的 0/O/1/I）
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def b64url_encode(data: bytes) -> str:
    """规范 base64url 编码：无填充、url-safe字符集。"""
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def canonical_json(obj: dict) -> str:
    """规范 JSON 序列化：键名排序、无空格、ensure_ascii=False。"""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def get_mac_key() -> bytes:
    """K = sha256(盐) 的字节，作为 HMAC 密钥。"""
    return hashlib.sha256(MAC_SALT.encode("utf-8")).digest()


def compute_mac(token_without_mac: dict, code: str) -> str:
    """两级 HMAC-SHA256：mac = HMAC(K, HMAC(K, canonical) + '|' + code)"""
    K = get_mac_key()
    canonical = canonical_json(token_without_mac)
    inner = hmac.new(K, canonical.encode("utf-8"), hashlib.sha256).hexdigest()
    outer_input = (inner + "|" + code).encode("utf-8")
    return hmac.new(K, outer_input, hashlib.sha256).hexdigest()


def generate_short_code() -> str:
    """生成16位短码（不含连字符），32字母表。"""
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(16))


def format_code(code: str) -> str:
    """格式化为 XXXX-XXXX-XXXX-XXXX。"""
    return f"{code[0:4]}-{code[4:8]}-{code[8:12]}-{code[12:16]}"


def code_hash_prefix(code: str) -> str:
    """f = sha256(码)[:16] hex，用作索引文件名。"""
    return hashlib.sha256(code.upper().encode("utf-8")).hexdigest()[:16]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_token(db_version: str, file_hash: str, exp: str, notes: str,
                 url: str = None, data_b64: str = None, typ: str = "data") -> dict:
    """构建不含 mac 的 token。"""
    token = {
        "v": db_version,
        "h": file_hash,
        "exp": exp,
        "iat": int(time.time()),
        "typ": typ,
    }
    if url:
        token["u"] = url
    if data_b64:
        token["data"] = data_b64
    if notes:
        token["notes"] = notes
    return token


def main():
    parser = argparse.ArgumentParser(description="生成嘌呤数据库更新密钥")
    parser.add_argument("--db", required=True, help="数据库 JSON 文件路径")
    parser.add_argument("--url", help="（通道②）更新包基地址或数据库下载地址")
    parser.add_argument("--offline", action="store_true", help="（通道③）生成离线自包含数据包")
    parser.add_argument("--long", action="store_true", help="生成长码 PUR- 格式（兼容模式），默认生成短码")
    parser.add_argument("--exp", required=True, help="密钥过期日期 (YYYY-MM-DD)")
    parser.add_argument("--notes", default="", help="更新说明（可选）")
    parser.add_argument("--count", type=int, default=1, help="短码生成数量（默认1）")
    parser.add_argument("--keys-dir", default="keys-out", help="短码索引文件输出目录（默认 keys-out）")
    parser.add_argument("--typ", default="data", choices=["data", "full"], help="升级类型：data=仅数据，full=数据+UI代码（默认data）")
    args = parser.parse_args()

    try:
        date.fromisoformat(args.exp)
    except ValueError:
        print("错误：--exp 日期格式应为 YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)

    if args.offline and args.url:
        print("错误：--offline 与 --url 互斥", file=sys.stderr)
        sys.exit(1)

    with open(args.db, "r", encoding="utf-8") as f:
        raw_json = f.read()
    db = json.loads(raw_json)
    version = db.get("db_version", "unknown")
    raw_bytes = raw_json.encode("utf-8")

    if args.offline:
        compressed = gzip.compress(raw_bytes, compresslevel=9)
        data_b64 = base64.b64encode(compressed).decode("ascii")
        file_hash = sha256_bytes(raw_bytes)
        token = build_token(version, file_hash, args.exp,
                            args.notes or f"离线更新包 {version}", data_b64=data_b64, typ="data")
        # 离线包用长码格式
        mac = compute_mac(token, "")
        token["mac"] = mac
        token_json = canonical_json(token)
        encoded = b64url_encode(token_json.encode("utf-8"))
        print(f"模式: 通道③离线包")
        print(f"数据库版本: {version}")
        print(f"SHA-256: {file_hash}")
        print(f"压缩后: {len(compressed)} 字节")
        print(f"\n离线密钥:\nPUR-{encoded}")
        return

    # 通道②
    file_hash = sha256_file(args.db)
    if not args.url:
        print("错误：通道②必须提供 --url（更新包基地址）", file=sys.stderr)
        sys.exit(1)

    if args.long:
        # 长码兼容模式
        token = build_token(version, file_hash, args.exp, args.notes, url=args.url, typ=args.typ)
        mac = compute_mac(token, "")
        token["mac"] = mac
        token_json = canonical_json(token)
        encoded = b64url_encode(token_json.encode("utf-8"))
        print(f"模式: 通道②长码（兼容）")
        print(f"数据库版本: {version}")
        print(f"SHA-256: {file_hash}")
        print(f"下载地址: {args.url}")
        print(f"\n长密钥:\nPUR-{encoded}")
        return

    # 短码模式（默认）
    os.makedirs(args.keys_dir, exist_ok=True)
    used_codes = set()
    print(f"模式: 通道②短码（16位）+ 托管索引")
    print(f"数据库版本: {version}")
    print(f"SHA-256: {file_hash}")
    print(f"基地址: {args.url}")
    print(f"升级类型: {args.typ}")
    print(f"生成数量: {args.count}")
    print(f"索引目录: {args.keys_dir}/")
    print("=" * 60)

    for i in range(args.count):
        # 生成唯一码
        while True:
            code = generate_short_code()
            if code not in used_codes:
                used_codes.add(code)
                break

        seq = i + 1
        token = build_token(version, file_hash, args.exp, args.notes,
                            url=args.url, typ=args.typ)
        token["seq"] = seq
        mac = compute_mac(token, code)
        token["mac"] = mac

        # 写索引文件
        f = code_hash_prefix(code)
        idx_path = os.path.join(args.keys_dir, f"{f}.json")
        with open(idx_path, "w", encoding="utf-8") as out:
            json.dump(token, out, ensure_ascii=False, indent=2)

        display = format_code(code)
        print(f"[{seq}/{args.count}] 短码: {display}")
        print(f"         索引: keys/{f}.json")
        print(f"         二维码内容: {display}")

    print("=" * 60)
    print(f"完成！将 {args.keys_dir}/ 目录上传到托管地址的 keys/ 子目录下。")
    print(f"用户在应用中输入短码即可更新。")


if __name__ == "__main__":
    main()
