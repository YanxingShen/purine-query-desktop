#!/usr/bin/env python3
"""
嘌呤数据库更新密钥生成工具（官方侧使用）
支持两种模式：
  通道②在线密钥：含下载地址，手机端联网拉取更新包
  通道③离线包：密钥内含 gzip 压缩的完整数据库，无需联网

用法（通道②）:
    python scripts/generate_update_key.py --db data/purine-db.json --url https://example.com/purine-db-v1.1.0.json --exp 2027-03-01

用法（通道③离线包）:
    python scripts/generate_update_key.py --db data/purine-db.json --offline --exp 2027-03-01

输出:
    PUR-<base64url编码的JSON令牌>
"""
import argparse
import base64
import gzip
import hashlib
import json
import sys
from datetime import date


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description="生成嘌呤数据库一次性更新密钥")
    parser.add_argument("--db", required=True, help="数据库 JSON 文件路径")
    parser.add_argument("--url", help="（通道②）数据库下载地址（静态托管/CDN）")
    parser.add_argument("--offline", action="store_true", help="（通道③）生成离线自包含数据包密钥")
    parser.add_argument("--exp", required=True, help="密钥过期日期 (YYYY-MM-DD)")
    parser.add_argument("--notes", default="", help="更新说明（可选）")
    args = parser.parse_args()

    # 校验过期日期
    try:
        date.fromisoformat(args.exp)
    except ValueError:
        print("错误：--exp 日期格式应为 YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)

    # 模式校验
    if args.offline and args.url:
        print("错误：--offline 与 --url 互斥，离线包不含下载地址", file=sys.stderr)
        sys.exit(1)
    if not args.offline and not args.url:
        print("错误：在线模式必须提供 --url，或使用 --offline 生成离线包", file=sys.stderr)
        sys.exit(1)

    # 读取数据库
    with open(args.db, "r", encoding="utf-8") as f:
        raw_json = f.read()
    db = json.loads(raw_json)
    version = db.get("db_version", "unknown")
    raw_bytes = raw_json.encode("utf-8")

    if args.offline:
        # 通道③：gzip 压缩后 base64 编码
        compressed = gzip.compress(raw_bytes, compresslevel=9)
        data_b64 = base64.b64encode(compressed).decode("ascii")
        file_hash = sha256_bytes(raw_bytes)
        token = {
            "v": version,
            "h": file_hash,
            "exp": args.exp,
            "data": data_b64,
            "notes": args.notes or f"离线更新包 {version}",
        }
        mode = "通道③离线包"
    else:
        # 通道②：含下载地址
        file_hash = sha256_file(args.db)
        token = {
            "v": version,
            "u": args.url,
            "h": file_hash,
            "exp": args.exp,
            "notes": args.notes,
        }
        mode = "通道②在线密钥"

    token_json = json.dumps(token, ensure_ascii=False, separators=(",", ":"))
    encoded = base64.urlsafe_b64encode(token_json.encode("utf-8")).decode("ascii").rstrip("=")

    print(f"模式:       {mode}")
    print(f"数据库版本: {version}")
    print(f"SHA-256:    {file_hash}")
    print(f"过期日期:    {args.exp}")
    if args.url:
        print(f"下载地址:    {args.url}")
    if args.offline:
        print(f"压缩前大小:  {len(raw_bytes)} 字节")
        print(f"压缩后大小:  {len(compressed)} 字节")
        print(f"密钥长度:    {len(encoded) + 4} 字符")
        print("注意：离线包密钥很长，仅适合复制粘贴，不适合二维码")
    print(f"\n更新密钥:\nPUR-{encoded}")


if __name__ == "__main__":
    main()
