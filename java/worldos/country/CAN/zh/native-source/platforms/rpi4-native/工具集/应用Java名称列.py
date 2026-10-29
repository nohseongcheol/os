#!/usr/bin/env python3
"""内置 Java 局部作用域 이름을 바꾼다. 字符串·주석·外部值 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

项目根 = Path(__file__).resolve().parents[1]
映射值 = json.loads((项目根 / '命名/Java名称列.json').read_text())
块片表达式 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
日志记录 = []
for 目录值 in ('源代码', '用户/Java', '中文Java'):
    for 路径 in sorted((项目根 / 目录值).rglob('*.java')):
        源代码 = 路径.read_text()
        块列列表 = list(块片表达式.finditer(源代码))
        已使用名称 = {块片条目.group() for 块片条目 in 块列列表 if re.search('[首位操作数-힣]', 块片条目.group())}
        文件映射 = {}
        for 上一个项目, 之后值 in 映射值.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            新建名称 = 之后值
            while 新建名称 in 已使用名称: 新建名称 = '局部作用域' + 新建名称
            文件映射[上一个项目] = 新建名称
        修改值 = []
        上一个块片 = ''
        for 块片条目 in 块列列表:
            词法用机器字 = 块片条目.group()
            if 词法用机器字.startswith(('//', '/*', '"', "'")): continue
            if 词法用机器字 in 文件映射 and 上一个块片 != '.':
                修改值.append((块片条目.start(), 块片条目.end(), 文件映射[词法用机器字]))
                日志记录.append((str(路径.relative_to(项目根)), 词法用机器字, 文件映射[词法用机器字]))
            上一个块片 = 词法用机器字
        for 运行, 结尾, 新建名称 in reversed(修改值): 源代码 = 源代码[:运行] + 新建名称 + 源代码[结尾:]
        if 修改值: 路径.write_text(源代码)
(项目根 / '命名/Java名称映射.tsv').write_text('文件\t이전\t이후\n' + ''.join('\t'.join(条目值)+'\n' for 条目值 in sorted(set(日志记录))))
print('Java 名称 引用 更改值:', len(日志记录))
