#!/usr/bin/env python3
"""中文 C 식별자만 UCN으로 옮긴다. 字符串·字符·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

词元值 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<标识符值>[^\W\d]\w*)', re.S | re.M)

def 转换值(源代码):
    def 替换值(是否相等):
        if 是否相等.lastgroup == '보존':
            return 是否相等[0]
        return ''.join(字符值 if ord(字符值) < 128 else
                       ('\\u%04x' if ord(字符值) <= 65535 else '\\U%08x') % ord(字符值)
                       for 字符值 in 是否相等[0])
    return 词元值.sub(替换值, 源代码)

def 执行命令():
    解析器 = argparse.ArgumentParser()
    解析器.add_argument('原始', type=Path)
    解析器.add_argument('输出', type=Path)
    实参 = 解析器.parse_args()
    for 文件 in sorted(实参.原始.rglob('*')):
        if 文件.suffix not in ('.c', '.h'):
            continue
        输出 = 实参.输出 / 文件.relative_to(实参.原始)
        输出.parent.mkdir(parents=True, exist_ok=True)
        新建源代码 = 转换值(文件.read_text())
        if not 输出.exists() or 输出.read_text() != 新建源代码:
            输出.write_text(新建源代码)

if __name__ == '__main__':
    执行命令()
