#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 已保留複製 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 測試用戶網路 import 虛擬機器

位置 = Path(__file__).resolve().parents[1]
規格 = importlib.util.spec_from_file_location('介質工具', 位置 / '工具集/創建存儲介質.py')
介質工具 = importlib.util.module_from_spec(規格)
規格.loader.exec_module(介質工具)

def 編輯值(計算機, 內容值):
    運行 = len(計算機.日誌記錄)
    計算機.串行值.sendall(('edit note.txt\n' + 內容值 + '\n.save\n').encode())
    return 計算機.等待狀態狀態('jkoros> ', 運行)

def 執行命令():
    結果 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 臨時值:
        介質值 = Path(臨時值) / 'files.img'
        介質工具.創建條目(介質值)
        計算機 = 虛擬機器(位置 / 'build/kernel.elf', 存儲裝置中型=介質值)
        try:
            計算機.命令('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            編輯值(計算機, 'generation-one')
            計算機.命令('sync', ['Sync: 0'])
            編輯值(計算機, 'generation-two')
            計算機.命令('sync', ['Sync: 0'])
            編輯值(計算機, 'unsynced-three')
            結果['save'] = 計算機.日誌記錄.decode('utf-8', 'replace')
        finally:
            計算機.關閉()
        計算機 = 虛擬機器(位置 / 'build/kernel.iso', 'iso', 存儲裝置中型=介質值)
        try:
            輸出 = 計算機.命令('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 輸出
            計算機.命令('cat stored.txt', ['saved-from-C'])
            結果['restore'] = 計算機.日誌記錄.decode('utf-8', 'replace')
        finally:
            計算機.關閉()
        資料 = bytearray(介質值.read_bytes())
        代次列列表 = [struct.unpack_from('<I', 資料, (1 + 編號 * 259) * 512 + 4)[0] for 編號 in (0, 1)]
        最新值 = 0 if 代次列列表[0] > 代次列列表[1] else 1
        資料[(1 + 最新值 * 259 + 3) * 512] ^= 1
        介質值.write_bytes(資料)
        計算機 = 虛擬機器(位置 / 'build/kernel.elf', 存儲裝置中型=介質值)
        try:
            計算機.命令('cat note.txt', ['generation-one'])
            計算機.命令('cat stored.txt', ['saved-from-C'])
            結果['checksum_fallback'] = 計算機.日誌記錄.decode('utf-8', 'replace')
        finally:
            計算機.關閉()
        其他介質 = Path(臨時值) / 'foreign.img'
        其他介質.write_bytes(bytes([0x5a]) * (2048 * 512))
        上一個項目 = hashlib.sha256(其他介質.read_bytes()).hexdigest()
        計算機 = 虛擬機器(位置 / 'build/kernel.elf', 存儲裝置中型=其他介質)
        try:
            計算機.命令('sync', ['Sync: -19'])
        finally:
            計算機.關閉()
        assert hashlib.sha256(其他介質.read_bytes()).hexdigest() == 上一個項目
        結果['foreign_disk_unchanged'] = True
    (位置 / 'build/持久化測試.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE 存儲值/ISO 재부팅/校驗和 恢復狀態/다른 介質值 비변경', flush=True)

if __name__ == '__main__':
    執行命令()
