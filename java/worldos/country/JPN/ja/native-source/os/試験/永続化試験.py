#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 保持済み複写 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 利用者通信網試験 import 仮想機械

位置 = Path(__file__).resolve().parents[1]
仕様 = importlib.util.spec_from_file_location('媒体道具要素', 位置 / '道具/記憶媒体作成.py')
媒体道具要素 = importlib.util.module_from_spec(仕様)
仕様.loader.exec_module(媒体道具要素)

def 編集値(機械, 内容物値):
    起動処理 = len(機械.履歴記録記録)
    機械.直列値.sendall(('edit note.txt\n' + 内容物値 + '\n.save\n').encode())
    return 機械.状況待合('jkoros> ', 起動処理)

def 命令実行():
    結果 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 一時値:
        媒体値 = Path(一時値) / 'files.img'
        媒体道具要素.入口作成(媒体値)
        機械 = 仮想機械(位置 / 'build/kernel.elf', 記憶装置中間容量=媒体値)
        try:
            機械.命令('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            編集値(機械, 'generation-one')
            機械.命令('sync', ['Sync: 0'])
            編集値(機械, 'generation-two')
            機械.命令('sync', ['Sync: 0'])
            編集値(機械, 'unsynced-three')
            結果['save'] = 機械.履歴記録記録.decode('utf-8', 'replace')
        finally:
            機械.閉鎖()
        機械 = 仮想機械(位置 / 'build/kernel.iso', 'iso', 記憶装置中間容量=媒体値)
        try:
            出力 = 機械.命令('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 出力
            機械.命令('cat stored.txt', ['saved-from-C'])
            結果['restore'] = 機械.履歴記録記録.decode('utf-8', 'replace')
        finally:
            機械.閉鎖()
        データ = bytearray(媒体値.read_bytes())
        世代一覧一覧 = [struct.unpack_from('<I', データ, (1 + 番号 * 259) * 512 + 4)[0] for 番号 in (0, 1)]
        最新値 = 0 if 世代一覧一覧[0] > 世代一覧一覧[1] else 1
        データ[(1 + 最新値 * 259 + 3) * 512] ^= 1
        媒体値.write_bytes(データ)
        機械 = 仮想機械(位置 / 'build/kernel.elf', 記憶装置中間容量=媒体値)
        try:
            機械.命令('cat note.txt', ['generation-one'])
            機械.命令('cat stored.txt', ['saved-from-C'])
            結果['checksum_fallback'] = 機械.履歴記録記録.decode('utf-8', 'replace')
        finally:
            機械.閉鎖()
        他方媒体 = Path(一時値) / 'foreign.img'
        他方媒体.write_bytes(bytes([0x5a]) * (2048 * 512))
        前回項目 = hashlib.sha256(他方媒体.read_bytes()).hexdigest()
        機械 = 仮想機械(位置 / 'build/kernel.elf', 記憶装置中間容量=他方媒体)
        try:
            機械.命令('sync', ['Sync: -19'])
        finally:
            機械.閉鎖()
        assert hashlib.sha256(他方媒体.read_bytes()).hexdigest() == 前回項目
        結果['foreign_disk_unchanged'] = True
    (位置 / 'build/永続化試験.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE 格納値/ISO 재부팅/検査和 状況復旧/다른 媒体値 비변경', flush=True)

if __name__ == '__main__':
    命令実行()
