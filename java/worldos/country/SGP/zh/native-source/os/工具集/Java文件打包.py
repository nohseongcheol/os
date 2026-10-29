#!/usr/bin/env python3
"""명시한 Java 源代码树/类值 파일을 启动 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 可执行束打包(条目列列表):
    文件条目列 = []
    名称列列表 = {'Hello.java'}
    显式名称列 = set()
    for 条目值 in 条目列列表:
        if '=' not in 条目值:
            raise ValueError('expected NAME=PATH: ' + 条目值)
        名称, 路径 = 条目值.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', 名称) or 名称 in 显式名称列:
            raise ValueError('invalid or duplicate file name: ' + 名称)
        显式名称列.add(名称)
        名称列列表.add(名称)
        数据 = Path(路径).read_bytes()
        if len(数据) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + 名称)
        文件条目列.append((名称.encode('ascii'), 数据))
    if len(名称列列表) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    结果 = bytearray(struct.pack('<4sI', b'JKJF', len(文件条目列)))
    结果.extend(bytes(72 * len(文件条目列)))
    for 数, (名称, 数据) in enumerate(文件条目列):
        struct.pack_into('<64sII', 结果, 8 + 数 * 72, 名称, len(结果), len(数据))
        结果.extend(数据)
    return bytes(结果)


if __name__ == '__main__':
    解析值 = argparse.ArgumentParser(description=__doc__)
    解析值.add_argument('-o', required=True)
    解析值.add_argument('files', nargs='*', help='NAME=PATH')
    实参 = 解析值.parse_args()
    try:
        数据 = 可执行束打包(实参.files)
        目的地址值 = Path(实参.o)
        if not 目的地址值.exists() or 目的地址值.read_bytes() != 数据:
            临时值 = 目的地址值.with_name(目的地址值.name + '.tmp')
            临时值.write_bytes(数据)
            临时值.replace(目的地址值)
    except (ValueError, OSError) as 错误:
        解析值.error(str(错误))
