// ============================================================
// 嘌呤查询 - Electron 预加载脚本（contextBridge 安全暴露）
// 注意：sandbox:false 时可在 preload 中使用 Node 模块。
// ============================================================
'use strict';

const { contextBridge, ipcRenderer } = require('electron');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

/**
 * 计算 SHA-256 十六进制摘要。
 * 支持 string | Buffer | Uint8Array | ArrayBuffer。
 */
function sha256(input) {
  try {
    let data;
    if (input == null) {
      data = Buffer.alloc(0);
    } else if (typeof input === 'string') {
      data = Buffer.from(input, 'utf8');
    } else if (Buffer.isBuffer(input)) {
      data = input;
    } else if (input instanceof Uint8Array) {
      data = Buffer.from(input.buffer, input.byteOffset, input.byteLength);
    } else if (input instanceof ArrayBuffer) {
      data = Buffer.from(input);
    } else if (ArrayBuffer.isView(input)) {
      data = Buffer.from(input.buffer, input.byteOffset, input.byteLength);
    } else {
      data = Buffer.from(String(input));
    }
    return crypto.createHash('sha256').update(data).digest('hex');
  } catch (e) {
    return null;
  }
}

/** 读取文件并计算 SHA-256（Promise） */
function sha256File(filePath) {
  return new Promise((resolve, reject) => {
    try {
      const stream = fs.createReadStream(filePath);
      const hash = crypto.createHash('sha256');
      stream.on('data', (chunk) => hash.update(chunk));
      stream.on('end', () => resolve(hash.digest('hex')));
      stream.on('error', (err) => reject(err));
    } catch (e) {
      reject(e);
    }
  });
}

/** 从 package.json 读取版本号（preload 中无法直接 require('electron').app） */
function getVersion() {
  try {
    const pkg = JSON.parse(
      fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8')
    );
    return pkg.version || '0.0.0';
  } catch (e) {
    return '0.0.0';
  }
}

contextBridge.exposeInMainWorld('electronAPI', {
  isDesktop: true,
  platform: process.platform,
  sha256,
  sha256File,
  getVersion
});
