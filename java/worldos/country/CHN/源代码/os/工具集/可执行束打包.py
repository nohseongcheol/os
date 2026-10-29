#!/usr/bin/env python3
"""명시한 用户 ELF만 读取 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 可执行束打包():
    解析值 = argparse.ArgumentParser()
    解析值.add_argument('-o', required=True)
    解析值.add_argument('files', nargs='+', help='名称=ELF경로')
    形参参数 = 解析值.parse_args()
    if len(形参参数.files) > 32:
        解析值.error('程序 最大值 32개')
    条目列列表 = []
    名称列列表 = set()
    for 条目值 in 形参参数.files:
        名称, 路径 = 条目值.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', 名称) or 名称 in 名称列列表:
            解析值.error('执行命令 이름이 잘못되었거나 중복됨: ' + 名称)
        名称列列表.add(名称)
        数据 = Path(路径).read_bytes()
        if len(数据) > 2 * 1024 * 1024:
            解析值.error('执行命令 파일이 너무 큼')
        条目列列表.append((名称.encode(), 数据))
    结果 = bytearray(8 + 24 * len(条目列列表))
    struct.pack_into('<II', 结果, 0, 0x50414b4a, len(条目列列表))
    for 编号, (名称, 数据) in enumerate(条目列列表):
        结果.extend(bytes((-len(结果)) % 16))
        struct.pack_into('<16sII', 结果, 8 + 编号 * 24, 名称, len(结果), len(数据))
        结果.extend(数据)
    Path(形参参数.o).write_bytes(结果)

if __name__ == '__main__':
    可执行束打包()
