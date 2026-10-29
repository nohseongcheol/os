#!/usr/bin/env python3
"""声明 고유번호와 UTF-8 字节值 위치로 内置 C 이름을 옮기는 일회성 이행 工具集.

外部值 구조체의 멤버, 字符串, C 표준 函数, 移植 규약은 보존한다.
입력은 更改值 之前值 소스에 대한 分析C名称列.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

项目根 = Path(__file__).resolve().parents[1]

def 执行命令():
    分析值 = json.loads((项目根/'build/한국어화/시언어분석.json').read_text())
    if 分析值['错误']: raise SystemExit('分析值 오류를 먼저 해결해야 합니다.')
    名称表 = json.loads((项目根/'命名/C名称列.json').read_text())
    标准定义 = set(json.loads((项目根/'命名/标准名称列.json').read_text()))
    声明表 = 分析值['声明']
    声明目标侧替换 = {唯一值:名称表[条目值['名称']] for 唯一值,条目值 in 声明表.items()
                if 条目值['名称'] in 名称表 and 条目值['名称'] not in 标准定义}
    连接状态表 = {条目值['名称']:名称表[条目值['名称']] for 条目值 in 声明表.values()
              if 条目值.get('连接')==4 and 条目值['种类值'] in (8,9)
              and 条目值['名称'] in 名称表 and 条目值['名称'] not in 标准定义}
    # 生成 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 连接 이름만 유지한다.
    头值 = ['/* 中文 源代码树 이름과 기존 计算机 连接 契约值. 자동 生成: 命名/C名称列.json */',
           '#ifndef 原生计算机连接名称列头部', '#define 原生计算机连接名称列头部']
    头值 += ['#define '+新建名称+' '+旧名称 for 旧名称,新建名称 in sorted(连接状态表.items())]
    头值 += ['#endif','']
    (项目根/'命名/计算机连接名称列.h').write_text('\n'.join(头值))
    更改列列表 = defaultdict(dict)
    for 文件,偏移值,名称,唯一值 in 分析值['引用']:
        if 唯一值 in 声明目标侧替换:
            更改列列表[文件][偏移值] = (名称,声明目标侧替换[唯一值])
    日志记录 = ['文件\t원래바이트위치\t이전이름\t한국어이름']
    忽略值 = []
    for 文件,更改值 in 更改列列表.items():
        路径 = Path(文件); 原始 = 路径.read_bytes(); 数据 = 原始
        for 偏移值,(旧名称,新建名称) in sorted(更改值.items(),reverse=True):
            结尾 = 偏移值+len(旧名称.encode())
            if 原始[偏移值:结尾] != 旧名称.encode():
                忽略值.append((str(路径.relative_to(项目根)),偏移值,旧名称));continue
            数据 = 数据[:偏移值]+新建名称.encode()+数据[结尾:]
            日志记录.append('{}\t{}\t{}\t{}'.format(路径.relative_to(项目根),偏移值,旧名称,新建名称))
        路径.write_bytes(数据)
    # 预处理源代码 매개변수는 AST의 선언으로 나타나지 않는다. 预处理源代码 줄만 보완한다.
    词法用机器字 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    宏值 = {条目值['名称']:名称表[条目值['名称']] for 条目值 in 声明表.values()
              if 条目值['种类值']==501 and 条目值['名称'] in 名称表 and 条目值['名称'] not in 标准定义}
    for 路径 in sorted({Path(条目值['文件']) for 条目值 in 声明表.values()}):
        多行内容 = 路径.read_text().splitlines(True); 是否继续状态 = False
        for 编号,行 in enumerate(多行内容):
            预处理源代码 = 是否继续状态 or bool(re.match(r'\s*#',行))
            是否继续状态 = 预处理源代码 and 行.rstrip().endswith('\\')
            if 预处理源代码:
                表 = 名称表 if re.match(r'\s*#\s*define\b',行) or 是否继续状态 else 宏值
                多行内容[编号] = 词法用机器字.sub(lambda 是否已匹配: 表.get(是否已匹配[0],是否已匹配[0]) if 是否已匹配[0] not in 标准定义 else 是否已匹配[0],行)
        路径.write_text(''.join(多行内容))
    # 각 内置 翻译源代码 단위에만 연결표를 넣는다. 外部值 배포본에는 전파하지 않는다.
    for 路径 in sorted({Path(条目值['文件']) for 条目值 in 声明表.values()}):
        if 路径.suffix not in ('.c','.cpp'):continue
        对端值 = '../' * len(路径.relative_to(项目根).parts[:-1]) + '命名/计算机连接名称列.h'
        路径.write_text('#include "'+对端值+'"\n'+路径.read_text())
    (项目根/'命名/C名称映射.tsv').write_text('\n'.join(日志记录)+'\n')
    (项目根/'build/한국어화/전처리참조.json').write_text(json.dumps(忽略值,ensure_ascii=False,indent=2)+'\n')
    print('更改值',len(日志记录)-1,'预处理源代码 재검토',len(忽略值),'计算机 连接',len(连接状态表))

if __name__=='__main__': 执行命令()
