#!/usr/bin/env python3
"""內建 Java 局部作用域 이름을 바꾼다. 字符串·주석·外部值 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

項目根 = Path(__file__).resolve().parents[1]
映射值 = json.loads((項目根 / '命名/Java名稱列.json').read_text())
塊片表達式 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
日誌記錄 = []
for 目錄值 in ('原始碼', '使用者/Java', '中文Java'):
    for 路徑 in sorted((項目根 / 目錄值).rglob('*.java')):
        原始碼 = 路徑.read_text()
        塊列列表 = list(塊片表達式.finditer(原始碼))
        已使用名稱 = {塊片條目.group() for 塊片條目 in 塊列列表 if re.search('[首位操作數-힣]', 塊片條目.group())}
        檔案映射 = {}
        for 上一個項目, 之後值 in 映射值.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            新建名稱 = 之後值
            while 新建名稱 in 已使用名稱: 新建名稱 = '局部作用域' + 新建名稱
            檔案映射[上一個項目] = 新建名稱
        修改值 = []
        上一個塊片 = ''
        for 塊片條目 in 塊列列表:
            詞法用機器字 = 塊片條目.group()
            if 詞法用機器字.startswith(('//', '/*', '"', "'")): continue
            if 詞法用機器字 in 檔案映射 and 上一個塊片 != '.':
                修改值.append((塊片條目.start(), 塊片條目.end(), 檔案映射[詞法用機器字]))
                日誌記錄.append((str(路徑.relative_to(項目根)), 詞法用機器字, 檔案映射[詞法用機器字]))
            上一個塊片 = 詞法用機器字
        for 運行, 結尾, 新建名稱 in reversed(修改值): 原始碼 = 原始碼[:運行] + 新建名稱 + 原始碼[結尾:]
        if 修改值: 路徑.write_text(原始碼)
(項目根 / '命名/Java名稱映射.tsv').write_text('檔案\t이전\t이후\n' + ''.join('\t'.join(條目值)+'\n' for 條目值 in sorted(set(日誌記錄))))
print('Java 名稱 引用 更改值:', len(日誌記錄))
