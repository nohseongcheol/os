#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 已保留复制 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 测试用户网络 import 虚拟机

位置 = Path(__file__).resolve().parents[1]
规格 = importlib.util.spec_from_file_location('介质工具', 位置 / '工具集/创建存储介质.py')
介质工具 = importlib.util.module_from_spec(规格)
规格.loader.exec_module(介质工具)

def 编辑值(计算机, 内容值):
    运行 = len(计算机.日志记录)
    计算机.串行值.sendall(('edit note.txt\n' + 内容值 + '\n.save\n').encode())
    return 计算机.等待状态状态('jkoros> ', 运行)

def 执行命令():
    结果 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 临时值:
        介质值 = Path(临时值) / 'files.img'
        介质工具.创建条目(介质值)
        计算机 = 虚拟机(位置 / 'build/kernel.elf', 存储装置中型=介质值)
        try:
            计算机.命令('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            编辑值(计算机, 'generation-one')
            计算机.命令('sync', ['Sync: 0'])
            编辑值(计算机, 'generation-two')
            计算机.命令('sync', ['Sync: 0'])
            编辑值(计算机, 'unsynced-three')
            结果['save'] = 计算机.日志记录.decode('utf-8', 'replace')
        finally:
            计算机.关闭()
        计算机 = 虚拟机(位置 / 'build/kernel.iso', 'iso', 存储装置中型=介质值)
        try:
            输出 = 计算机.命令('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 输出
            计算机.命令('cat stored.txt', ['saved-from-C'])
            结果['restore'] = 计算机.日志记录.decode('utf-8', 'replace')
        finally:
            计算机.关闭()
        数据 = bytearray(介质值.read_bytes())
        代次列列表 = [struct.unpack_from('<I', 数据, (1 + 编号 * 259) * 512 + 4)[0] for 编号 in (0, 1)]
        最新值 = 0 if 代次列列表[0] > 代次列列表[1] else 1
        数据[(1 + 最新值 * 259 + 3) * 512] ^= 1
        介质值.write_bytes(数据)
        计算机 = 虚拟机(位置 / 'build/kernel.elf', 存储装置中型=介质值)
        try:
            计算机.命令('cat note.txt', ['generation-one'])
            计算机.命令('cat stored.txt', ['saved-from-C'])
            结果['checksum_fallback'] = 计算机.日志记录.decode('utf-8', 'replace')
        finally:
            计算机.关闭()
        其他介质 = Path(临时值) / 'foreign.img'
        其他介质.write_bytes(bytes([0x5a]) * (2048 * 512))
        上一个项目 = hashlib.sha256(其他介质.read_bytes()).hexdigest()
        计算机 = 虚拟机(位置 / 'build/kernel.elf', 存储装置中型=其他介质)
        try:
            计算机.命令('sync', ['Sync: -19'])
        finally:
            计算机.关闭()
        assert hashlib.sha256(其他介质.read_bytes()).hexdigest() == 上一个项目
        结果['foreign_disk_unchanged'] = True
    (位置 / 'build/持久化测试.json').write_text(json.dumps(结果, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE 存储值/ISO 재부팅/校验和 恢复状态/다른 介质值 비변경', flush=True)

if __name__ == '__main__':
    执行命令()
