#!/usr/bin/env python3
"""中文 C 식별자만 UCN으로 옮긴다. 字符串·字元·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

詞元值 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<標識符值>[^\W\d]\w*)', re.S | re.M)

def 轉換值(原始碼):
    def 替換值(是否相等):
        if 是否相等.lastgroup == '보존':
            return 是否相等[0]
        return ''.join(字元值 if ord(字元值) < 128 else
                       ('\\u%04x' if ord(字元值) <= 65535 else '\\U%08x') % ord(字元值)
                       for 字元值 in 是否相等[0])
    return 詞元值.sub(替換值, 原始碼)

def 執行命令():
    解析器 = argparse.ArgumentParser()
    解析器.add_argument('原始', type=Path)
    解析器.add_argument('輸出', type=Path)
    實參 = 解析器.parse_args()
    for 檔案 in sorted(實參.原始.rglob('*')):
        if 檔案.suffix not in ('.c', '.h'):
            continue
        輸出 = 實參.輸出 / 檔案.relative_to(實參.原始)
        輸出.parent.mkdir(parents=True, exist_ok=True)
        新建原始碼 = 轉換值(檔案.read_text())
        if not 輸出.exists() or 輸出.read_text() != 新建原始碼:
            輸出.write_text(新建原始碼)

if __name__ == '__main__':
    執行命令()
